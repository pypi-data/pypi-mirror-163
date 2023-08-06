import pandas as pd
import numpy as np
import re
import json
import argparse
import tldextract
import sys
import urllib
import ast
import traceback
import goodfaith.core.graph
import goodfaith.core.scope
from pandas.io.json import json_normalize
from urllib.parse import urlparse

def parseUrlRoot(urlvalue):
        try:
            urlvalue = urlvalue.lstrip('[')
            urlvalue = urlvalue.rstrip(']')
            cleanurl = urlparse(urlvalue)#.netloc
            cleanurl = cleanurl.hostname
            return str(cleanurl)
        except:
            # If urlparse due to weird characters like "[", utilize generic url to avoid downstream issues.
            # TODO: I'm sure there is probably a better way to handle this.
            urlvalue = "failed"
            cleanurl = urlparse(urlvalue)#.netloc
            cleanurl = cleanurl.hostname
            return str(cleanurl)

def parseUrlBase(urlvalue):
    # Normalize URLs to avoid duplicate urls if it is http or https and has standard ports. Was discovering duplicate urls with and without port.
    try:
        urlvalue = urlvalue.lstrip('[')
        urlvalue = urlvalue.rstrip(']')
        baseurl = urlparse(urlvalue)
        if (baseurl.port == 443 or baseurl.port == 80):
            baseurl = baseurl.scheme + '://' + baseurl.hostname + baseurl.path
        else:
            baseurl = baseurl.scheme + '://' + baseurl.netloc + baseurl.path
        return str(baseurl)
    except:
        # If urlparse fails, utilize generic url to avoid downstream issues.
        # TODO: I'm sure there is probably a better way to handle this.
        
        urlvalue = "failed"
        baseurl = urlparse(urlvalue)
        baseurl = baseurl.scheme + '://' + baseurl.hostname + baseurl.path
        return str(baseurl)

def processEnrichURLs(programScope, dfAllURLs): # dataframe requires domain column
    
    programName = programScope['program']
    
    ScopeInURLs, ScopeInGithub, ScopeInWild, ScopeInGeneral, ScopeInIP, ScopeOutURLs, ScopeOutGithub, ScopeOutWild, ScopeOutGeneral, ScopeOutIP = extrapolateScope(programScope['program'],programScope['in_scope'],programScope['out_of_scope'])

    dfAllURLs['domain'] = dfAllURLs['url'].apply(parseUrlRoot)
    dfAllURLs['baseurl'] = dfAllURLs['url'].apply(parseUrlBase)
    dfAllURLs['program'] = programName
    
    # Remove rows that failed cleanup (parseUrlRoot and parseUrlBase)
    dfAllURLs = dfAllURLs[dfAllURLs.domain != 'failed']
    dfAllURLs = dfAllURLs[dfAllURLs.baseurl != 'failed']
    
    # Scope mapper
    mapperIn = {True: 'in', False: 'other'}  # in = within the defined scope
    mapperOut = {True: 'out', False: 'in'} # out = explicitly out of scope
    mapperWild = {True: 'wild', False: 'out'} # wild - within the wildcard scope
    # other = not in scope but not explicitly excluded
    
    # This checks to determine whether a url is explicitly defined as out-of-scope
    dfAllURLs['scopeOut'] = dfAllURLs.domain.str.lower().isin([x.lower() for x in ScopeOutGeneral]).map(mapperOut)
    # This checks to determine whether a url is explicitly defined as in-scope
    dfAllURLs['scopeIn'] = dfAllURLs.domain.str.lower().isin([x.lower() for x in ScopeInGeneral]).map(mapperIn)
    
    # This section checks for wildcard scopes and determines whether a url is included within the wildcard scope
    lstWildIn = []
    for wild in ScopeInWild:
        wild = re.sub(r'^.*?\*\.', '', wild)
        lstWildIn.append(wild.lower())
        #print(wild)
    
    dfAllURLs['scopeInWild'] = dfAllURLs.domain.str.lower().str.endswith(tuple(lstWildIn)).map(mapperWild)
    
    # This section checks for wildcard scopes and determines whether a url is included within the wildcard scope
    lstWildOut = []
    for wild in ScopeOutWild:
        wild = re.sub(r'^.*?\*\.', '', wild)
        lstWildOut.append(wild.lower())

    dfAllURLs['scopeOutWild'] = dfAllURLs.domain.str.lower().str.endswith(tuple(lstWildOut)).map(mapperOut)
    
    # This section creates a normalized scope field to track in, out, wild, or other
    conditions = [
        (dfAllURLs['scopeOut'] == 'out'),
        (dfAllURLs['scopeOutWild'] == 'out'),
        (dfAllURLs['scopeIn'] == 'in') & (dfAllURLs['scopeOut'] != 'out') & (dfAllURLs['scopeOutWild'] != 'out'),
        (dfAllURLs['scopeInWild'] == 'wild') & (dfAllURLs['scopeIn'] != 'in') & (dfAllURLs['scopeOut'] != 'out') & (dfAllURLs['scopeOutWild'] != 'out'),
        (dfAllURLs['scopeIn'] == 'other') & (dfAllURLs['scopeInWild'] != 'wild') & (dfAllURLs['scopeIn'] != 'in') & (dfAllURLs['scopeOut'] != 'out') & (dfAllURLs['scopeOutWild'] != 'out')
    ]
    
    # Each of these values maps to the equivalent condition listed
    values = ['out', 'out', 'in', 'wild', 'other']                                                                           
    
    # Create a new column and assign the values specific to the conditions.
    # TODO - This could potentially miss items since it is a select. Need to perform some searches on whether or not scope column is populated after using this for a while.
    dfAllURLs['scope'] = np.select(conditions, values)
    return dfAllURLs

def boundaryGuard(dfAllURLs, outputDir, programScope, quietMode, debugMode, outputType):
    
    for item in programScope:
        try:
            programName = item['program']

            dfAllURLs = processEnrichURLs(item, dfAllURLs)

            # File path that does not contain explicitly out-of-scope items
            storeModPathUrl = outputDir + programName + '-urls-other.txt'
            # File path that only contains explicitly in-scope urls
            storeInPathUrl = outputDir + programName + '-urls-in-full.txt'
            # File path that only contains explicitly in-scope urls
            storeBasePathUrl = outputDir + programName + '-urls-in-base.txt'
            storeInDomains = outputDir + programName + '-domains-in.txt'
            storeOutPathUrl = outputDir + programName + '-urls-out.txt'
            detailedURLOutput = outputDir + programName + '-details.csv'
            statsFile = outputDir + programName + '-stats.txt'
    
            # Create DataFrames containing sorted URLs
            dfURLsIn = dfAllURLs[(dfAllURLs['scope'] == 'in') | (dfAllURLs['scope'] == 'wild')]
            dfURLsMod = dfAllURLs[dfAllURLs['scope'] == 'other']
#            dfURLsMod = dfAllURLs[(dfAllURLs['scope'] != 'out') | (dfAllURLs['scope'] != 'in') | (dfAllURLs['scope'] != 'wild')]
            dfURLsOut = dfAllURLs[dfAllURLs['scope'] == 'out']
    
            if (outputDir != 'NoOutput'):
                if (len(dfURLsIn.index) > 0):
                    # Output URLs that are in-scope
                    dfURLsIn['url'].drop_duplicates().to_csv(storeInPathUrl, header=None, index=False, sep='\n')
                    # This only outputs the base URL so that it can be used for fuzzing
                    dfURLsIn['baseurl'].drop_duplicates().to_csv(storeBasePathUrl, header=None, index=False, sep='\n')
                    # Output domains that are in-scope
                    dfURLsIn['domain'].drop_duplicates().to_csv(storeInDomains, header=None, index=False, sep='\n')
                if (len(dfURLsMod.index) > 0):
                    # Output URLs that are not explicitly out-of-scope
                    dfURLsMod['url'].drop_duplicates().to_csv(storeModPathUrl, header=None, index=False, sep='\n')
                if (len(dfURLsOut.index) > 0):
                    # Output URLs that are explicitly out-of-scope
                    dfURLsOut['url'].drop_duplicates().to_csv(storeOutPathUrl, header=None, index=False, sep='\n')
                if (len(dfAllURLs.index) > 0):
                    # Output detailed summary file
                    dfAllURLs.to_csv(detailedURLOutput, columns=['url','domain','baseurl','program','scope'], index=False)

                try:
                    with open(statsFile, "a") as file_object:
                        file_object.write('Total number of urls: ' + str(len(dfAllURLs['url'].drop_duplicates())))
                        file_object.write('\n')
                        file_object.write('Number of urls not in scope but not explicitly out-of-scope: ' + str(len(dfURLsMod['url'].drop_duplicates())))
                        file_object.write('\n')
                        file_object.write('Number of urls in-scope: ' + str(len(dfURLsIn['url'].drop_duplicates())))
                        file_object.write('\n')
                        file_object.write('Number of urls out-of-scope: ' + str(len(dfURLsOut['url'].drop_duplicates())))
                        file_object.write('\n')
                        file_object.write('Number of unique domains: ' + str(len(dfAllURLs['domain'].drop_duplicates())))
                        file_object.write('\n')
                except:
                    if quietMode is False:
                        print('Failed to write stats file.')
    
            if (outputType == 'full_url'):
                # Output the full URLs to console/stdout
                dfURLsIn['url'].drop_duplicates().to_csv(sys.stdout, header=None, index=False, sep='\n')
            elif (outputType == 'base_url'):
                # Output the base URLs to console/stdout
                dfURLsIn['baseurl'].drop_duplicates().to_csv(sys.stdout, header=None, index=False, sep='\n')
            elif (outputType == 'domain'):
                # Output the domains to console/stdout
                dfURLsIn['domain'].drop_duplicates().to_csv(sys.stdout, header=None, index=False, sep='\n')
            else:
                # This code should never hit due to prior data validation, but just in case, default to full URLs.
                dfURLsIn['url'].drop_duplicates().to_csv(sys.stdout, header=None, index=False, sep='\n')
            
            if quietMode is False:
                # Output metrics within console
                print('\n')
                print('Total number of urls: ' + str(len(dfAllURLs['url'].drop_duplicates())))
                print('Number of urls not explicitly out-of-scope: ' + str(len(dfURLsMod['url'].drop_duplicates())))
                print('Number of urls in-scope: ' + str(len(dfURLsIn['url'].drop_duplicates())))
                print('Number of urls out-of-scope: ' + str(len(dfURLsOut['url'].drop_duplicates())))
                print('Number of unique domains: ' + str(len(dfAllURLs['domain'].drop_duplicates())))
        except:
            if quietMode is False:
                print('Program: ' + programName + ' failed to process.')
                if debugMode is True:
                    print(traceback.format_exc())
    return dfAllURLs

def processSingleDomain(domainName):
    domainList = []
    ext = tldextract.extract(domainName)
    if (ext.suffix is not ''):
        rootDomain = ext.domain + '.' + ext.suffix
        domainList.append(rootDomain)
        if (ext.subdomain is not ''):
            subDomain = ext.subdomain
            subs = subDomain.split('.')
            subLength = len(subs) - 1
            while subLength >= 0:
                rootDomain = subs[subLength] + '.' + rootDomain
                domainList.append(rootDomain)
                subLength = subLength - 1
    else:
        rootDomain = ext.domain
        domainList.append(rootDomain)
        subDomain = ext.subdomain
        subs = subDomain.split('.')
        subLength = len(subs) - 1
        while subLength >= 0:
            rootDomain = subs[subLength] + '.' + rootDomain
            domainList.append(rootDomain)
            subLength = subLength - 1
    return domainList

def cleanupScopeGithub(dfIn):
    matchString = 'github.com'
    matches = []
    for match in dfIn:
        match = re.search("(?P<url>https?://[^\s]+)", match)
        if match is None:
            continue
        else:
            match = match.group('url')
            if matchString in match:
                matches.append(match)
            else:
                continue
    return matches
def cleanupScopeStrict(dfIn):
    matchString = 'github.com'
    matches = []
    for match in dfIn:
        #if matchString in match:
        match = re.search("(?P<url>https?://[^\s]+)", match)
        if match is None:
            continue
        else:
            match = match.group('url')
            if matchString in match:
                continue
            else:
                matches.append(match)
    return matches

def cleanupScopeWild(dfIn):
    matchString = '\*.'
    matches = []
    for match in dfIn:
        
        # There was a bug in the regex where it was dropping anything prior to the asterisk so it has been updated. A wildcard match must now begin with a wildcard.
        # TODO: Add functionality to include wildcards in the middle of strings.
        # Old version: (?P<url>[*][^\s|\,]+)
        
        match = re.search("(?P<url>^[*][^\s|\,]+)", match)
   
        if match is None:
            continue
        else:
            match = match.group('url')
            if (match != '*.'):
                # This check is to fix an issue for program mistakes where it has '*. domain.com'. The space in there causes the search to be *. which will include all URLs.
                matches.append(match)
    return matches

def cleanupScopeIP(dfIn):
    matchString = '\*.'
    matches = []
    for match in dfIn:
        
        match = re.search("(?P<url>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|))", match)
        
        if match is None:
            continue
        else:
            match = match.group('url')
            matches.append(match)
    return matches

def cleanupScopeGeneral(dfIn):
    matchStringSpace = ' '
    matchStringGit = 'github.com'
    matchStringUrl = 'http'
    matchStringWild = '\*.'
    matchStringDot = '.'
    matches = []
    for match in dfIn:
        matchWild = re.search("(?P<url>[*][^\s|\,]+)", match)
        matchDot = re.search("(?P<url>[.][^\s]+)", match)
        matchIP = re.search("(?P<url>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|))", match)
        if matchStringGit in match:
            continue
        elif matchStringSpace in match:
            continue
        elif matchStringUrl in match:
            url = urlparse(match)
            match = url.netloc
            matches.append(match)
            continue
        elif matchIP is not None:
            continue
        elif matchWild is not None:
            match = match.replace('*.','')
            matches.append(match)
            continue
        elif matchDot is None:
            continue
        else:
            matches.append(match)
    return matches

def extrapolateScope(programName, listscopein, listscopeout):
    ScopeInURLs = cleanupScopeStrict(listscopein)
    ScopeInGithub = cleanupScopeGithub(listscopein)
    ScopeInWild = cleanupScopeWild(listscopein)
    ScopeInGeneral = cleanupScopeGeneral(listscopein)
    ScopeInIP = cleanupScopeIP(listscopein)
    ScopeOutURLs = cleanupScopeStrict(listscopeout)
    ScopeOutGithub = cleanupScopeGithub(listscopeout)
    ScopeOutWild = cleanupScopeWild(listscopeout)
    ScopeOutGeneral = cleanupScopeGeneral(listscopeout)
    ScopeOutIP = cleanupScopeIP(listscopeout)
    return ScopeInURLs, ScopeInGithub, ScopeInWild, ScopeInGeneral, ScopeInIP, ScopeOutURLs, ScopeOutGithub, ScopeOutWild, ScopeOutGeneral, ScopeOutIP

def loadScope(scopeFile):
    programData = open(scopeFile)
    programScope = json.load(programData)
    return programScope

def parseScope(inputScope):
    targetData = []
    if not inputScope:
        targetData.append('failed')
        return targetData
    smallAll = str(inputScope)[1:-1]
    scopeLength = len(inputScope)
    smallData = ast.literal_eval(smallAll)

    if (scopeLength > 1):
        for item in smallData:
            if item.get('target') is not None:
                targetData.append(item.get('target'))
            if item.get('asset_identifier') is not None:
                targetData.append(item.get('asset_identifier'))
            # Intigriti file references JSON element as endpoint
            if item.get('endpoint') is not None:
                targetData.append(item.get('endpoint'))
        return targetData
    else:
        if smallData.get('target') is not None:
            targetData.append(smallData.get('target'))
        if smallData.get('asset_identifier') is not None:
            targetData.append(smallData.get('asset_identifier'))
        # Intigriti file references JSON element as endpoint
        if smallData.get('endpoint') is not None:
            targetData.append(smallData.get('endpoint'))
        return targetData

# Retrieve Bulk Programs
def bulkLoad(bulkPlatform):
    if (bulkPlatform == 'bugcrowd'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/bugcrowd_data.json'
    if (bulkPlatform == 'hackerone'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/hackerone_data.json'
    if (bulkPlatform == 'intigriti'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/intigriti_data.json'
    if (bulkPlatform == 'yeswehack'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/yeswehack_data.json'
    if (bulkPlatform == 'federacy'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/federacy_data.json'
    if (bulkPlatform == 'hackenproof'):
        filePath = 'https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/master/data/hackenproof_data.json'

    with urllib.request.urlopen(filePath) as url:
        data = json.loads(url.read().decode())

    # These functions normalize the program names 
    def parseProgramUrl(programUrl):
        programName = programUrl.rsplit('/', 1)[-1]
        programName = ''.join(e for e in programName if e.isalnum())
        return programName

    def parseProgramName(programName):
        programName = ''.join(e for e in programName if e.isalnum())
        return programName

    # Count the scopes processed
    counter = 0
    for scope in data:
        counter = counter + 1
        # Normalize the JSON keys
        if (bulkPlatform == 'bugcrowd'):
            scope['program'] = parseProgramUrl(scope['url'])
        if (bulkPlatform == 'hackerone'):
            scope['program'] = parseProgramName(scope['handle'])
        if (bulkPlatform == 'intigriti'):
            scope['program'] = parseProgramName(scope['company_handle'])
        if (bulkPlatform == 'yeswehack'):
            scope['program'] = parseProgramName(scope['id'])
        if (bulkPlatform == 'federacy'):
            scope['program'] = parseProgramUrl(scope['url'])
        if (bulkPlatform == 'hackenproof'):
            scope['program'] = parseProgramUrl(scope['url'])

    dfPublicPrograms = pd.json_normalize(data)
    dfPublicPrograms['platform'] = bulkPlatform
    dfPublicPrograms['invite'] = 'public'
    dfPublicPrograms['in_scope'] = dfPublicPrograms['targets.in_scope'].apply(parseScope)
    dfPublicPrograms['out_of_scope'] = dfPublicPrograms['targets.out_of_scope'].apply(parseScope)
    # Make a copy of DataFrame to only include relevant columns.
    # Can always add additional columns in the future.
    dfBulkLoad = dfPublicPrograms[['program','in_scope','out_of_scope','platform','invite']].copy()
    platformJSON = dfBulkLoad.to_json(orient='records')
    platformData = json.loads(platformJSON)
    return platformData, counter