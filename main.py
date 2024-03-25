import json

def injectConstantVariables(tempgtmparams, gtmjson):
    newtempgtmparams = set()
    constantVariables = {}

    for variable in gtmjson['containerVersion']['variable']:
        if (variable['type'] == 'c'):
            constantVariables[variable['name']] = variable['parameter'][0]['value']

    for gtmparam in tempgtmparams:
        if (gtmparam[0] == '{' and gtmparam[1] == '{' and gtmparam[-1] == '}' and gtmparam[-2] == '}'):
            newgtmparam = gtmparam[2:-2]
            newtempgtmparams.add(constantVariables[newgtmparam])
        else:
            newtempgtmparams.add(gtmparam)

    return newtempgtmparams

# This was written by Kenny
def main(name):

    # Check if they entered arguments
    # if len(sys.argv) < 2:
    #     print("You must give two arguments! First argument is  GTM container json export and second is bigquery table json export")
    #     exit(1)
    #
    try:
        f1 = open("gtmjson.json", "r")
        f2 = open("bqjson.json", "r")
    except:
        f = open("results.txt", "w")
        f.write("Files not found\n")
        f.write("Inside the folder that this executable is in, name the GTM json \"gtmjson.json\" and the Big Query json \"bqjson\"\n(or just gtmjson and bqjson if you explorer hides your file types from you)")
        exit(1)

    f = open("results.txt", "w")

    gtmjson = json.load(f1)
    bqjson = json.load(f2)

    gtmGA4TagEventNames = set()
    bqEventNames = set()

    # The logic for getting all the event names from the GTM json
    gtmtags = gtmjson['containerVersion']['tag']
    gtmGA4TagParameters = []
    for tag in gtmtags:
        if (tag['type'] == 'gaawe'):
             gtmGA4TagParameters.append(tag['parameter'])

    for param in gtmGA4TagParameters:
        for paramDictionary in param:
            if (paramDictionary['key'] == 'eventName'):
                gtmGA4TagEventNames.add(paramDictionary['value'])

    # The logic for getting all the vent names from the big query json
    for event in bqjson:
        bqEventNames.add(event['event_name'])

    # See how they differ (only things in GTM that aren't in BiqQuery)
    difference = bqEventNames.difference(gtmGA4TagEventNames)

    # Here is the logic for filtering out all the names that we don't care about
    dontcareSet = {
        'page_view',
        '',
    }

    if (len(difference) == 0):
        f.write("Couldn't find any events in Big Query that aren't in GTM")
    else:
        f.write("These are events in Big Query that aren't in GTM as GA4 events (at least didn't happen in the date range of the query)\n")
        f.write(str(difference))
        f.write("\n\n")

    exit(0)


if __name__ == '__main__':
    main('PyCharm')

