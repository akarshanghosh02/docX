# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:37:46 2021
@author: akarshan.ghosh
"""

from xml.dom import minidom
import ComponentName
import readCSV

schema_dict, bsSchemaDefination, boSchemaDefination, boLifeCycle,boLifeCycleState, dataArea, uiMap, batchCntlComp, portalComp,final_bo_life_cycle = {},{}, {}, {}, {}, {}, {}, {}, {}, {}
algorithm, algoType, algorithmSoftParameter, algorithmTypeSoftParameter = [], [], {}, {}
componentList,query,query12 = [],[],[]
charType, list_of_component, messages_list, adjTypeComp, featCnfgComp = {}, {}, [], {}, {}
FKRefComp, adjTypePrfComp, appSvcComp, billMsgComp, billSegTypComp = {}, {}, {}, {}, {}
bktCnfgComp, calcLineCatTypComp, busFlgTypComp, calcGrpComp = {}, {}, {}, {}
iwsSvcSOAPComp, fieldComp, caseTypComp, final_case_lfc = {}, {}, {}, {}
leadEvntTypComp, lookupComp, mainObjComp, mgmtContentComp, migrPlnComp = {}, {}, {}, {}, {}
migrReqComp, navKeyComp, navOptComp, ntfTypComp, perCntTypComp = {}, {}, {}, {}, {}
rateSchedComp, initiativeComp, salesRepComp, toDoTypComp = {}, {}, {}, {}

df = '';
# This function take the bundle and extract it's component, component type, BoData and etc.
def extractBundleData(filename=None):
    global componentList
    init()
    dataFrame=df;
    entities = dataFrame["root"]["bundle"]["entities"]

    for entity in entities:

        if len(entities) == 1:

            sequence = entities["sequence"]
            componentType = entities['mo']
            component = entities['pk1']
        else:
            sequence = entity["sequence"]
            componentType = entity['mo']
            component = entity['pk1']

        if sequence is None or componentType is None or component is None:
            print("Error: Required keys not found in 'entity' dictionary.")
            continue

        entityList = [{'sequence':sequence}, {'componentType':componentType}, {'component':component}]
        componentList.append(entityList)

        # if boData is not None:
        #     getBOData(boData, componentType, component)

    list_of_component["components"] = componentList

def fetchData(xml_data):
    entities = xml_data["root"]["bundle"]["entities"]
    for entity in entities:
        componentType = entity['mo']
        component = entity['pk1']
        boData = entity['boData']

        if boData is not None:
            getBOData(boData, componentType, component)

def getBOData(boData, componentType, component):
    # boDataChildren = boData.childNodes

    component_functions = {
        "CONTENT ZONE": lambda: getZoneValue(boData,component),
        # "SCRIPT": lambda: getScriptData(boDataChildren, component),
        # "F1-BUS SVC": lambda: getBusiness_Service_Object_Data(boDataChildren, component, componentType),
        # "ALG TYPE": lambda: (algoType.append(component + "\n"), getAlgoTypeSoftParam(boDataChildren, component)),
        # "ALGORITHM": lambda: (algorithm.append(component + "\n"), getAlgoSoftParam(boDataChildren, component)),
        # "CHAR TYPE": lambda: getCharType(boDataChildren, component),
        # "F1-MESSAGE": lambda: getMessages(boDataChildren),
        # "F1-BUS OBJ": lambda: getBusiness_Service_Object_Data(boDataChildren, component, componentType),
        # "F1-DATA AREA": lambda: getDataArea(boDataChildren, component, componentType),
        # "F1-UI MAP": lambda: getUiMap(boDataChildren, component, componentType),
        # "BATCH CNTL": lambda: getBatchCntl(boDataChildren, component),
        # "PORTAL": lambda: getPortal(boDataChildren, component),
        # "ADJ TYPE": lambda: getAdjType(boDataChildren, component),
        # "WFM SYSTEM": lambda: getFeatCnfg(boDataChildren, component),
        # "FK REF": lambda: getFKRef(boDataChildren, component),
        # "ADJ TYPE PRF": lambda: getAdjTypePrf(boDataChildren, component),
        # "APP SERVICE": lambda: getAppService(boDataChildren, component),
        # "BILL MESSAGE": lambda: getBillMsg(boDataChildren, component),
        # "BILL SEG TYP": lambda: getBillSegTyp(boDataChildren, component),
        # "F1-BKTCONFIG": lambda: getBktCnfg(boDataChildren, component),
        # "C1-CL-CAT": lambda: getCalcLineCatTyp(boDataChildren, component),
        # "F1-BUSFLGTYP": lambda: getBusFlgTyp(boDataChildren, component),
        # "C1-CALC-GRP": lambda: getCalcGrp(boDataChildren, component),
        # "F1-IWSSVC": lambda: getIwsSvcSOAP(boDataChildren, component),
        # "FIELD": lambda: getField(boDataChildren, component),
        # "CASE TYPE": lambda: getCaseTyp(boDataChildren, component),
        # "C1-LEAD-EVTY": lambda: getLeadEvntTyp(boDataChildren, component),
        # "LOOKUP": lambda: getLookup(boDataChildren, component),
        # "MAIN OBJ": lambda: getMainObj(boDataChildren, component),
        # "F1-MAN CONT": lambda: getMgmtContent(boDataChildren, component),
        # "F1-MIGRPLAN": lambda: getMigrPln(boDataChildren, component),
        # "F1-MIGRREQ": lambda: getMigrReq(boDataChildren, component),
        # "NAV KEY": lambda: getNavKey(boDataChildren, component),
        # "NAV OPT": lambda: getNavOpt(boDataChildren, component),
        # "C1-NTF-TYPE": lambda: getNtfTyp(boDataChildren, component),
        # "C1-PERCNT-TY": lambda: getPerCntTyp(boDataChildren, component),
        # "RATE SCHED": lambda: getRateSched(boDataChildren, component),
        # "C1-INITIATIV": lambda: getInitiative(boDataChildren, component),
        # "C1-SALESREP": lambda: getSalesRep(boDataChildren, component),
        # "TO DO TYPE": lambda: getToDoTyp(boDataChildren, component)
    }

    if componentType in component_functions:
        component_functions[componentType]()

def getDataArea(boDataChildren, component, componentType):
    description = {}
    schema = None
    for childNode in boDataChildren:
        if childNode.nodeName == 'schema':
            bsNode = childNode.childNodes
            for node in bsNode:
                if node.nodeName == 'schemaDefinition':
                    schema = node.firstChild.data
        if childNode.nodeName == 'description':
            description[childNode.nodeName] = childNode.lastChild.data
        if description and schema is not None:
            if componentType == "F1-DATA AREA":
                dataArea[component] = [description, schema]


def getZoneValue(boData, component):
    boDataChildren = boData['zoneParameter']
    list_of_queries=[]
    #TO-DO return list of queries in the zone
    for childNode in boDataChildren:
        if childNode['parameterName'] == 'ASQL':
            asql = childNode['parameterValue']
            asql = asql.replace("\n", " ")
            asql = component + "\n" + asql.upper()
            list_of_queries.append(asql)

        if childNode['parameterName'] == 'BSQL':
            bsql = childNode['parameterValue']
            bsql = bsql.replace("\n", " ")
            bsql = component + "\n" + bsql.upper()
            list_of_queries.append(bsql)

    return list_of_queries




def getScriptData(boDataChildren, component):
    label_flag = False
    # loop through the boData node
    script_step=boDataChildren['scriptStep']
    script_schema=boDataChildren['schema']
    script_data_area=boDataChildren['scriptDataArea']
    script_long_description=boDataChildren['longDescription']
    script_detail_description = boDataChildren['detailDescription']
    for step in script_step:
        sort_sequence=step['sortSequence']
        step_type=step['stepType']

        if step_type == 'LABL':
            edit_data_area=step['text']
        else:
            edit_data_area = step['editDataArea']


        script_steps = edit_data_area.replace("\n", " ")
        script_steps = script_steps.replace(";", ";\n")
        key = component + ComponentName.seperator + sort_sequence
        # schema_dict is defined as globally to store all the scripts values
        schema_dict[key] = script_steps
    schema_dict['description']=script_long_description
    schema_dict['schema']=script_schema
    script_schema['script_data_area']=script_data_area
    return schema_dict




def getBusiness_Service_Object_Data(boDataChildren, component, componentType):
    bo_bs = {}

    bo_bs['schemaDefinition']=boDataChildren['schema']['schemaDefinition']
    bo_bs['description']=boDataChildren['description'] if 'description' in boDataChildren and boDataChildren['description'] else None
    bo_bs['applicationServiceId']=boDataChildren['applicationServiceId'] if 'applicationServiceId' in boDataChildren and boDataChildren['applicationServiceId'] else None
    bo_bs['maintenanceObject']=boDataChildren['maintenanceObject'] if 'maintenanceObject' in boDataChildren and boDataChildren['maintenanceObject'] else None
    bo_bs['longDescription'] = boDataChildren['longDescription'] if 'longDescription' in boDataChildren and boDataChildren['longDescription'] else None
    bo_bs['businessObjectAlgorithm']=boDataChildren['businessObjectAlgorithm'] if 'businessObjectAlgorithm' in boDataChildren and boDataChildren['businessObjectAlgorithm'] else None
    bo_bs['businessObjectOption']=boDataChildren['businessObjectAlgorithm'] if 'businessObjectAlgorithm' in boDataChildren and boDataChildren['businessObjectAlgorithm'] else None
    bo_bs['businessObjectStatus']=boDataChildren['businessObjectAlgorithm'] if 'businessObjectAlgorithm' in boDataChildren and boDataChildren['businessObjectAlgorithm'] else None

    boLifeCycleStatus=boDataChildren['businessObjectStatus'] if 'businessObjectStatus' in boDataChildren and boDataChildren['businessObjectStatus'] else None

    for lifeCycleState in boLifeCycleStatus:

        status = None
        bo_lfc_gen = {}
        bo_life_cycle_algo_list = []
        bo_life_cycle_nxtstatus_list = []
        bo_life_cycle_status_option_list = []

        status=lifeCycleState['status']if 'status' in lifeCycleState and lifeCycleState['status'] else None
        bo_lfc_gen['description']=lifeCycleState['description'] if 'description' in lifeCycleState and lifeCycleState['description'] else None
        bo_lfc_gen['longDescription'] = lifeCycleState['longDescription'] if 'longDescription' in lifeCycleState and lifeCycleState['longDescription'] else None
        bo_lfc_gen['condition'] = lifeCycleState['condition'] if 'condition' in lifeCycleState and lifeCycleState['condition'] else None
        bo_lfc_gen['transitoryStatus'] = lifeCycleState['transitoryStatus'] if 'transitoryStatus' in lifeCycleState and lifeCycleState['transitoryStatus'] else None
        bo_lfc_gen['accessMode'] = lifeCycleState['accessMode'] if 'accessMode' in lifeCycleState and lifeCycleState['accessMode'] else None
        bo_lfc_gen['alert'] = lifeCycleState['alert'] if 'alert' in lifeCycleState and lifeCycleState['alert'] else None
        bo_lfc_gen['monitorProcess'] = lifeCycleState['monitorProcess'] if 'monitorProcess' in lifeCycleState and lifeCycleState['monitorProcess'] else None
        bo_lfc_gen['sortSequence'] = lifeCycleState['sortSequence'] if 'sortSequence' in lifeCycleState and lifeCycleState['sortSequence'] else None
        bo_lfc_gen['statusReasonExistence'] = lifeCycleState['statusReasonExistence'] if 'statusReasonExistence' in lifeCycleState and lifeCycleState['statusReasonExistence'] else None


        bo_life_cycle_algo_list.append(lifeCycleState["businessObjectStatusAlgorithm"] if 'businessObjectStatusAlgorithm' in lifeCycleState and lifeCycleState['businessObjectStatusAlgorithm'] else None)
        bo_life_cycle_nxtstatus_list.append(lifeCycleState['businessObjectStatusTransitionRule']if 'businessObjectStatusTransitionRule' in lifeCycleState and lifeCycleState['businessObjectStatusTransitionRule'] else None)
        bo_life_cycle_status_option_list.append(lifeCycleState['businessObjectStatusOption']if 'businessObjectStatusOption' in lifeCycleState and lifeCycleState['businessObjectStatusOption'] else None)


        boLifeCycle = {
            'Algorithm': bo_life_cycle_algo_list,
            'nxtstatus': bo_life_cycle_nxtstatus_list,
            'statusoption': bo_life_cycle_status_option_list
        }

        boLifeCycleState[status] = [bo_lfc_gen, boLifeCycle]

    bo_bs['metaInfo']=[boLifeCycleState]
    return bo_bs



def getCaseTyp(boDataChildren, component):
    caseTypInfo = {}
    caseTyp = {}
    case_typ_algo_list = []
    case_typ_char_list = []
    # Loop through all childNodes
    for childNode in boDataChildren:
        # First get common fields
        if childNode.nodeName == 'caseType':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'personUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'accountUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'premiseUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'businessObject':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'applicationServiceId':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'callbackPhoneUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'responsibleUserUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'contactInstructionsUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'contactInformationUsage':
            caseTypInfo[childNode.nodeName] = childNode.lastChild.data

        # Get extra fields and add to dict
        if childNode.nodeName == 'caseTypeAlgorithm':
            caseTypAlgo = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    caseTypAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'caseTypeSystemEvent':
                    caseTypAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'algorithm':
                    caseTypAlgo[node.nodeName] = node.lastChild.data
            case_typ_algo_list.append(caseTypAlgo)
            caseTyp['caseTypAlgo'] = case_typ_algo_list

        # Get extra fields and add to dict
        if childNode.nodeName == 'characteristicTypeCaseType':
            caseTypChar = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sortSequence':
                    caseTypChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicType':
                    caseTypChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'isRequired':
                    caseTypChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'shouldUseAsDefault':
                    caseTypChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicValue':
                    caseTypChar[node.nodeName] = node.lastChild.data
            case_typ_char_list.append(caseTypChar)
            caseTyp['caseTypChar'] = case_typ_char_list

        if childNode.nodeName == 'caseStatus':
            caseStatInfo = {}
            caseLifeCycle = {}
            case_lfc_list = []
            case_lfc_algo_list = []
            case_lfc_nxt_stat_list = []
            case_lfc_char_rule_list = []
            for node in childNode.childNodes:
                if node.nodeName == 'status':
                    status = node.lastChild.data
                    caseStatInfo[node.nodeName] = status
                if node.nodeName == 'script':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'accessMode':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'statusCondition':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sortSequence':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'alertFlag':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'transitoryFlag':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'batchControl':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'statusLabel':
                    caseStatInfo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'longDescription':
                    caseStatInfo[node.nodeName] = node.lastChild.data

                if node.nodeName == 'caseStatusAlgorithm':
                    caseLfcAlgo = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'sequence':
                            caseLfcAlgo[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'caseStatusSystemEvent':
                            caseLfcAlgo[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'algorithm':
                            caseLfcAlgo[nd.nodeName] = nd.lastChild.data
                    case_lfc_algo_list.append(caseLfcAlgo)
                    caseLifeCycle['caseLfcAlgo'] = case_lfc_algo_list

                if node.nodeName == 'caseStatusCharacteristicRule':
                    caseLfcCharRule = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'characteristicType':
                            caseLfcCharRule[nd.nodeName] = nd.lastChild.data
                    case_lfc_char_rule_list.append(caseLfcCharRule)
                    caseLifeCycle['caseLfcCharRule'] = case_lfc_char_rule_list

                if node.nodeName == 'caseStatusTransitionRule':
                    nxtState = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'nextStatus':
                            nxtState[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'transitionRole':
                            nxtState[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'sortSequence':
                            nxtState[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'shouldUseAsDefault':
                            nxtState[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'transitionCondition':
                            nxtState[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'nextStatus2':
                            nxtState[nd.nodeName] = nd.lastChild.data
                    case_lfc_nxt_stat_list.append(nxtState)
                    caseLifeCycle['nxtState'] = case_lfc_nxt_stat_list

            case_lfc_list.append(caseStatInfo)
            case_lfc_list.append(caseLifeCycle)
            final_case_lfc[status] = case_lfc_list

    caseTypComp[component] = [caseTypInfo, caseTyp]


def getAdjType(boDataChildren, component):
    adjTypeInfo = {}
    adjType = {}
    adj_type_char_list = []
    adj_type_algo_list = []
    adj_type_temp_char_list = []

    # Loop through all childNodes
    for childNode in boDataChildren:
        # First get common fields
        if childNode.nodeName == 'adjustmentType':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'adjustmentAmountType':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'distributionCode':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'currency':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'defaultAmount':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'autopay1099':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'autopayRequestType':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'adjustmentFreezeOption':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'approvalProfile':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'descriptionOnBill':
            adjTypeInfo[childNode.nodeName] = childNode.lastChild.data

        # Get extra fields and add to dict
        if childNode.nodeName == 'adjustmentTypeCharacteristic':
            adjTypeChar = {}
            for node in childNode.childNodes:
                if node.nodeName == 'characteristicType':
                    adjTypeChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicValue':
                    adjTypeChar[node.nodeName] = node.lastChild.data
            adj_type_char_list.append(adjTypeChar)
            adjType['adjTypeChar'] = adj_type_char_list

        if childNode.nodeName == 'adjustmentTypeAlgorithm':
            adjTypeAlgo = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    adjTypeAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'adjustmentTypeAlgorithmEntity':
                    adjTypeAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'algorithm':
                    adjTypeAlgo[node.nodeName] = node.lastChild.data
            adj_type_algo_list.append(adjTypeAlgo)
            adjType['adjTypeAlgo'] = adj_type_algo_list

        if childNode.nodeName == 'adjustmentTypeTemplateCharacteristic':
            adjTypeTempChar = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sortSequence':
                    adjTypeTempChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicType':
                    adjTypeTempChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'isRequired':
                    adjTypeTempChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'shouldUseAsDefault':
                    adjTypeTempChar[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicValue':
                    adjTypeTempChar[node.nodeName] = node.lastChild.data
            adj_type_temp_char_list.append(adjTypeTempChar)
            adjType['adjTypeTempChar'] = adj_type_temp_char_list
    adjTypeComp[component] = [adjTypeInfo, adjType]


def getAdjTypePrf(boDataChildren, component):
    adjTypePrfInfo = {}
    adjTypePrf = {}
    adj_type_prf_list = []

    # Loop through all childNodes
    for childNode in boDataChildren:
        # First get common fields
        if childNode.nodeName == 'adjustmentTypeProfile':
            adjTypePrfInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            adjTypePrfInfo[childNode.nodeName] = childNode.lastChild.data

        # Get extra fields and add to dict
        if childNode.nodeName == 'adjustmentTypeAdjustmentTypeProfile':
            adjTypeAdjTypePrf = {}
            for node in childNode.childNodes:
                if node.nodeName == 'adjustmentType':
                    adjTypeAdjTypePrf[node.nodeName] = node.lastChild.data
            adj_type_prf_list.append(adjTypeAdjTypePrf)
            adjTypePrf['adjTypePrf'] = adj_type_prf_list
    adjTypePrfComp[component] = [adjTypePrfInfo, adjTypePrf]


def getAppService(boDataChildren, component):
    appSvcInfo = {}
    appSvc = {}
    app_svc_mode_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'applicationServiceId':
            appSvcInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            appSvcInfo[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'applicationServiceAccessMode':
            appSvcMode = {}
            for node in childNode.childNodes:
                if node.nodeName == 'accessMode':
                    appSvcMode[node.nodeName] = node.lastChild.data
            app_svc_mode_list.append(appSvcMode)
            appSvc['appSvcMode'] = app_svc_mode_list
    appSvcComp[component] = [appSvcInfo, appSvc]


def getBktCnfg(boDataChildren, component):
    bktCnfgInfo = {}
    bktCnfg = {}
    bkt_cnfg_value_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'bucketConfiguration':
            bktCnfgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            bktCnfgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'bucketType':
            bktCnfgInfo[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'bucketConfigurationValue':
            bktcnfgvalue = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    bktcnfgvalue[node.nodeName] = node.lastChild.data
                if node.nodeName == 'startRange':
                    bktcnfgvalue[node.nodeName] = node.lastChild.data
                if node.nodeName == 'endRange':
                    bktcnfgvalue[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    bktcnfgvalue[node.nodeName] = node.lastChild.data
            bkt_cnfg_value_list.append(bktcnfgvalue)
            bktCnfg['bktCnfgValue'] = bkt_cnfg_value_list
    bktCnfgComp[component] = [bktCnfgInfo, bktCnfg]


def getIwsSvcSOAP(boDataChildren, component):
    iwsSvcSOAPInfo = {}
    iwsSvcSOAP = {}
    iws_svc_soap_opt_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'iwsName':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'webSvcClass':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'isTracing':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'isActive':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'shouldDebug':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'postError':
            iwsSvcSOAPInfo[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'iwsServiceOperation':
            iwsSvcSOAPOpt = {}
            for node in childNode.childNodes:
                if node.nodeName == 'operationName':
                    iwsSvcSOAPOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'schemaName':
                    iwsSvcSOAPOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'schemaType':
                    iwsSvcSOAPOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'transactionType':
                    iwsSvcSOAPOpt[node.nodeName] = node.lastChild.data
            iws_svc_soap_opt_list.append(iwsSvcSOAPOpt)
            iwsSvcSOAP['iwsSvcSOAPOpt'] = iws_svc_soap_opt_list
    iwsSvcSOAPComp[component] = [iwsSvcSOAPInfo, iwsSvcSOAP]


def getCalcLineCatTyp(boDataChildren, component):
    calcLineCatTypInfo = {}
    calcLineCatTyp = {}
    calc_line_cat_value_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'calcLineCategoryType':
            calcLineCatTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            calcLineCatTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            calcLineCatTypInfo[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'calcLineCategoryValue':
            calcLineCatValue = {}
            for node in childNode.childNodes:
                if node.nodeName == 'calcLineCategoryValue':
                    calcLineCatValue[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    calcLineCatValue[node.nodeName] = node.lastChild.data
            calc_line_cat_value_list.append(calcLineCatValue)
            calcLineCatTyp['calcLineCatValue'] = calc_line_cat_value_list
    calcLineCatTypComp[component] = [calcLineCatTypInfo, calcLineCatTyp]


def getFeatCnfg(boDataChildren, component):
    featCnfgInfo = {}
    featCnfg = {}
    feat_cnfg_opt_list = []
    feat_cnfg_msg_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'workforceManagementSystem':
            featCnfgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'featureType':
            featCnfgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            featCnfgInfo[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'featureConfigurationOption':
            featCnfgOpt = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    featCnfgOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'optionType':
                    featCnfgOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'value':
                    featCnfgOpt[node.nodeName] = node.lastChild.data
            feat_cnfg_opt_list.append(featCnfgOpt)
            featCnfg['featCnfgOpt'] = feat_cnfg_opt_list

        if childNode.nodeName == 'featureConfigurationMessage':
            featCnfgMsg = {}
            for node in childNode.childNodes:
                if node.nodeName == 'workforceManagementMessageCategory':
                    featCnfgMsg[node.nodeName] = node.lastChild.data
                if node.nodeName == 'wfmMessage':
                    featCnfgMsg[node.nodeName] = node.lastChild.data
                if node.nodeName == 'messageCategory':
                    featCnfgMsg[node.nodeName] = node.lastChild.data
                if node.nodeName == 'messageNumber':
                    featCnfgMsg[node.nodeName] = node.lastChild.data
            feat_cnfg_msg_list.append(featCnfgMsg)
            featCnfg['featCnfgMsg'] = feat_cnfg_msg_list
    featCnfgComp[component] = [featCnfgInfo, featCnfg]


def getBillMsg(boDataChildren, component):
    billMsgInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'billMessage':
            billMsgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            billMsgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'messagePriority':
            billMsgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'insert':
            billMsgInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'messageOnBill':
            billMsgInfo[childNode.nodeName] = childNode.lastChild.data
    billMsgComp[component] = [billMsgInfo]


def getField(boDataChildren, component):
    fieldInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'field':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'fieldScale':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'f1Translatable':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'isSigned':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longLabel':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'dataType':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'isWorkField':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'fieldPrecision':
            fieldInfo[childNode.nodeName] = childNode.lastChild.data
    fieldComp[component] = [fieldInfo]


def getBusFlgTyp(boDataChildren, component):
    busFlgTypInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'businessFlagType':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'businessFlagPriority':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'standardName':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'businessObjectXMLDataArea':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'relatedTransactionBO':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'businessFlagTypeStatus':
            busFlgTypInfo[childNode.nodeName] = childNode.lastChild.data
    busFlgTypComp[component] = [busFlgTypInfo]


def getCalcGrp(boDataChildren, component):
    calcGrpInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'calcGroup':
            calcGrpInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            calcGrpInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            calcGrpInfo[childNode.nodeName] = childNode.lastChild.data
    calcGrpComp[component] = [calcGrpInfo]


def getBillSegTyp(boDataChildren, component):
    billSegTypInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'billSegmentType':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'billSegmentCreationAlgorithm':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'billSegmentFinancialAlgorithm':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'billSegmentGetConsumptionAlgorithm':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'autoCancelAlgorithm':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'informationAlgorithm':
            billSegTypInfo[childNode.nodeName] = childNode.lastChild.data
    billSegTypComp[component] = [billSegTypInfo]


def getFKRef(boDataChildren, component):
    FKRefInfo = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'foreignKeyReference':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'table':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'navigationOption':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'programType':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'infoProgram':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'contextMenu':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'zone':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'searchNavigationKey':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'searchType':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'searchTooltip':
            FKRefInfo[childNode.nodeName] = childNode.lastChild.data
    FKRefComp[component] = [FKRefInfo]


def getBatchCntl(boDataChildren, component):
    batchCntlinfo = {}
    batch_cntl_para_list = []
    batch_cntl_algo_list = []
    batchcntl = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'longDescription':
            batchCntlinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'batchControlType':
            batchCntlinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'programType':
            batchCntlinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'batchControlParameter':
            batchCntlpara = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    batchCntlpara[node.nodeName] = node.lastChild.data
                if node.nodeName == 'batchParameterName':
                    batchCntlpara[node.nodeName] = node.lastChild.data
                if node.nodeName == 'batchParameterValue':
                    batchCntlpara[node.nodeName] = node.lastChild.data
                if node.nodeName == 'isRequired':
                    batchCntlpara[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    batchCntlpara[node.nodeName] = node.lastChild.data
            batch_cntl_para_list.append(batchCntlpara)
            batchcntl['Parameters'] = batch_cntl_para_list
        if childNode.nodeName == 'batchControlAlgorithm':
            batchCntlalgo = {}
            for node in childNode.childNodes:
                if node.nodeName == 'batchControlSystemEvent':
                    batchCntlalgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sequence':
                    batchCntlalgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'algorithm':
                    batchCntlalgo[node.nodeName] = node.lastChild.data
            batch_cntl_algo_list.append(batchCntlalgo)
            batchcntl['Algorithm'] = batch_cntl_algo_list
    batchCntlComp[component] = [batchCntlinfo, batchcntl]


def getPortal(boDataChildren, component):
    portalinfo = {}
    portal_zone_list = []
    portal_option_list = []
    portal = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'portalType':
            portalinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            portalinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'programComponent':
            portalinfo[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'portalZone':
            portalZone = {}
            for node in childNode.childNodes:
                if node.nodeName == 'zone':
                    portalZone[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sortSequence':
                    portalZone[node.nodeName] = node.lastChild.data
                if node.nodeName == 'canDisplay':
                    portalZone[node.nodeName] = node.lastChild.data
            portal_zone_list.append(portalZone)
            portal['zone'] = portal_zone_list
        if childNode.nodeName == 'portalOption':
            portalOpt = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    portalOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'portalOptionType':
                    portalOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'portalOptionValue':
                    portalOpt[node.nodeName] = node.lastChild.data
            portal_option_list.append(portalOpt)
            portal['option'] = portal_option_list
    portalComp[component] = [portalinfo, portal]


def getUiMap(boDataChildren, component, componentType):
    description = None
    schema = None
    htmldef = None
    for childNode in boDataChildren:
        if childNode.nodeName == 'schema':
            bsNode = childNode.childNodes
            for node in bsNode:
                if node.nodeName == 'schemaDefinition':
                    schema = node.firstChild.data
        if childNode.nodeName == 'description':
            description = childNode.firstChild.data
        if childNode.nodeName == 'htmlDefn':
            htmldef = childNode.firstChild.data
        if description is not None and schema is not None and htmldef is not None:
            if componentType == "F1-UI MAP":
                uiMap[component] = [schema, description, htmldef]
                return


def getAlgoSoftParam(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    algoSoftParam=boDataChildren['algorithmVersion']['algorithmParameter']
    comnFlds['algorithm']=boDataChildren['algorithm']
    comnFlds['algorithmType'] = boDataChildren['algorithmType']
    comnFlds['description'] = boDataChildren['description']

    for parm in algoSoftParam:
        extFlds1 = {}
        extFlds1['sequence']=parm['sequence'] if 'sequence' in parm and parm['sequence'] is not None else None
        extFlds1['value'] = parm['value'] if 'value' in parm and parm['value'] is not None else None
        extFlds1['effectiveDate']=parm['effectiveDate'] if 'effectiveDate' in parm and parm['effectiveDate'] is not None else None

        extFlds_lst1.append(extFlds1)
        extFlds['algoPara'] = extFlds_lst1
    algorithmSoftParameter[component] = [comnFlds, extFlds]
    return algorithmSoftParameter




def getAlgoTypeSoftParam(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    comnFlds['algorithmType']=boDataChildren['algorithmType']
    comnFlds['longDescription'] = boDataChildren['longDescription']
    comnFlds['programType'] = boDataChildren['programType']
    comnFlds['algorithmEntity'] = boDataChildren['algorithmEntity']
    comnFlds['programName'] = boDataChildren['programName']
    comnFlds['description'] = boDataChildren['description']

    algoTypeParameter=boDataChildren['algorithmTypeParameter']
    for param in algoTypeParameter:
        extFlds1 = {}
        extFlds1['sequence'] = param['sequence']
        extFlds1['parameterLabel'] = param['parameterLabel']
        extFlds1['isParameterRequired'] = param['isParameterRequired']

        extFlds_lst1.append(extFlds1)
        extFlds['algoTypPara'] = extFlds_lst1

    algorithmTypeSoftParameter[component] = [comnFlds, extFlds]
    return algorithmTypeSoftParameter



def getCharType(boDataChildren, component):
    charType_map = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'characteristicType':
            charType_map[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            charType_map[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'characteristicTypeFlag':
            charType_map[childNode.nodeName] = childNode.lastChild.data if childNode.lastChild else ""
    charType[component] = charType_map


def getMessages(boDataChildren):
    messageCategory = None
    messageNumber = None
    messageDesc = None
    for child in boDataChildren:
        if child.nodeName == 'messageCategory':
            messageCategory = child.lastChild.data
        elif child.nodeName == 'messageNumber':
            messageNumber = child.lastChild.data
        elif child.nodeName == 'messageText':
            messageDesc = child.lastChild.data

        if messageDesc != None and messageNumber != None and messageCategory != None:
            messages_list.append([messageCategory, messageNumber, messageDesc])
            return


def getLeadEvntTyp(boDataChildren, component):
    comnFlds = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'leadEventType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'businessObjectDataArea':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'relatedTransactionBO':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
    leadEvntTypComp[component] = [comnFlds]


def getLookup(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    look_val_list = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'fieldName':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'objectPropertyName':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'lookupValue':
            lookVal = {}
            for node in childNode.childNodes:
                if node.nodeName == 'fieldValue':
                    lookVal[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    lookVal[node.nodeName] = node.lastChild.data
                if node.nodeName == 'valueName':
                    lookVal[node.nodeName] = node.lastChild.data
            look_val_list.append(lookVal)
            extFlds['lookVal'] = look_val_list
    lookupComp[component] = [comnFlds, extFlds]


def getMainObj(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    extFlds_lst3 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'maintenanceObject':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'serviceName':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'maintenanceObjectTable':
            mainObjTbl = {}
            for node in childNode.childNodes:
                if node.nodeName == 'table':
                    mainObjTbl[node.nodeName] = node.lastChild.data
                if node.nodeName == 'tableRole':
                    mainObjTbl[node.nodeName] = node.lastChild.data
                if node.nodeName == 'parentConstraintId':
                    mainObjTbl[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(mainObjTbl)
            extFlds['mainObjTbl'] = extFlds_lst1

        if childNode.nodeName == 'maintenanceObjectAlgorithm':
            mainObjAlgo = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    mainObjAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'event':
                    mainObjAlgo[node.nodeName] = node.lastChild.data
                if node.nodeName == 'algorithm':
                    mainObjAlgo[node.nodeName] = node.lastChild.data
            extFlds_lst2.append(mainObjAlgo)
            extFlds['mainObjAlgo'] = extFlds_lst2

        if childNode.nodeName == 'maintenanceObjectOption':
            mainObjOpt = {}
            for node in childNode.childNodes:
                if node.nodeName == 'maintenanceObjectOptionType':
                    mainObjOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sequence':
                    mainObjOpt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'maintenanceObjectOptionValue':
                    mainObjOpt[node.nodeName] = node.lastChild.data
            extFlds_lst3.append(mainObjOpt)
            extFlds['mainObjOpt'] = extFlds_lst3
    mainObjComp[component] = [comnFlds, extFlds]


def getMgmtContent(boDataChildren, component):
    comnFlds = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'managedContentCd':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'managedContentType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'manageContentData':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
    mgmtContentComp[component] = [comnFlds]


def getMigrPln(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    for childNode in boDataChildren:
        # First get common fields
        if childNode.nodeName == 'migrationPlan':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        # Get extra fields and add to dict
        if childNode.nodeName == 'migrationPlanInstruction':
            migrPlnInstruc = {}
            for node in childNode.childNodes:
                if node.nodeName == 'instructionSequence':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'instructionType':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'parentInstructionSequence':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'businessObject':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'nextMigrationPlan':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'traversalCriteriaType':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'constraintId':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'referringConstraintOwner':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sqlTraversalCriteria':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'xPathTraversalCriteria':
                    migrPlnInstruc[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(migrPlnInstruc)
            extFlds['migrPlnInstruc'] = extFlds_lst1
    # Merge common fields and extra fields to main dict
    migrPlnComp[component] = [comnFlds, extFlds]


def getMigrReq(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'migrationRequest':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'migrationRequestInstruction':
            migrReqInstruc = {}
            for node in childNode.childNodes:
                if node.nodeName == 'migrationPlan':
                    migrReqInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'selectionType':
                    migrReqInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'sqlStatementText':
                    migrReqInstruc[node.nodeName] = node.lastChild.data
                if node.nodeName == 'migrationRequestInstructionEntity':
                    for nd in node.childNodes:
                        if nd.nodeName == 'primaryKeyValue1':
                            migrReqInstruc[nd.nodeName] = nd.lastChild.data
            extFlds_lst1.append(migrReqInstruc)
            extFlds['migrReqInstruc'] = extFlds_lst1
    migrReqComp[component] = [comnFlds, extFlds]


def getNavKey(boDataChildren, component):
    comnFlds = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'navigationKey':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'overriddenNavigationKey':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'openWindowOptions':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'programComponent':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'urlLocation':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'overrideUrl':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
    navKeyComp[component] = [comnFlds]


def getNavOpt(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'navigationOption':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'subQueryZone':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'usageType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'navigationMode':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'searchType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'searchNavigationKey':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'targetNavigationKey':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'tabPageNavigationKey':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'navigationOptionType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'multiQueryZone':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'script':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'navigationOptionUsage':
            navOptUsage = {}
            for node in childNode.childNodes:
                if node.nodeName == 'navigationOptionUsage':
                    navOptUsage[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(navOptUsage)
            extFlds['navOptUsage'] = extFlds_lst1

        if childNode.nodeName == 'navigationOptionContext':
            navOptCntxt = {}
            for node in childNode.childNodes:
                if node.nodeName == 'field':
                    navOptCntxt[node.nodeName] = node.lastChild.data
                if node.nodeName == 'isKeyField':
                    navOptCntxt[node.nodeName] = node.lastChild.data
            extFlds_lst2.append(navOptCntxt)
            extFlds['navOptCntxt'] = extFlds_lst2
    navOptComp[component] = [comnFlds, extFlds]


def getNtfTyp(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'notificationType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'notificationControl':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'notificationRecipient':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'notificationPushSub':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'serviceTaskType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'selfServiceNotificationType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'notificationTypeAlgorithm':
            extFlds1 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    extFlds1[node.nodeName] = node.lastChild.data
                if node.nodeName == 'systemEvent':
                    extFlds1[node.nodeName] = node.lastChild.data
                if node.nodeName == 'algorithm':
                    extFlds1[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(extFlds1)
            extFlds['ntfTypAlgo'] = extFlds_lst1

        if childNode.nodeName == 'notificationTypePersonContactType':
            extFlds2 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'personContactType':
                    extFlds2[node.nodeName] = node.lastChild.data
            extFlds_lst2.append(extFlds2)
            extFlds['ntfTypPer'] = extFlds_lst2
    ntfTypComp[component] = [comnFlds, extFlds]


def getPerCntTyp(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'personContactType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'allowPersonContactStatus':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'detailedDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'formatAlgorithm':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'allowDoNotDisturb':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'communicationRoutingMethod':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'deliveryTypes':
            extFlds1 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'deliveryType':
                    extFlds1[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(extFlds1)
            extFlds['perCntTypDelvTyp'] = extFlds_lst1

        if childNode.nodeName == 'personContactTypeCharacteristic':
            extFlds2 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'characteristicValueForeignKey1':
                    extFlds2[node.nodeName] = node.lastChild.data
            extFlds_lst2.append(extFlds2)
            extFlds['perCntTypChar'] = extFlds_lst2
    perCntTypComp[component] = [comnFlds, extFlds]


def getRateSched(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    extFlds_lst3 = []
    extFlds_lst4 = []
    extFlds_lst5 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'rateSchedule':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'allowRVProration':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'rateScheduleType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'allowEstimates':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'frequency':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'serviceType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'rateScheduleVersion':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'currency':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'rateSelectionDateOption':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'rateScheduleDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'meterConfigurationType':
            for node in childNode.childNodes:
                if node.nodeName == 'meterConfigurationTypes':
                    extFlds1 = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'meterConfigurationType':
                            extFlds1[nd.nodeName] = nd.lastChild.data
                    extFlds_lst1.append(extFlds1)
                    extFlds['rtSchMeterCnfgTyp'] = extFlds_lst1

        if childNode.nodeName == 'ratePostProcessing':
            for node in childNode.childNodes:
                if node.nodeName == 'ratePostProcessingRules':
                    extFlds2 = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'sequence':
                            extFlds2[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'description':
                            extFlds2[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'calculationGroup':
                            extFlds2[nd.nodeName] = nd.lastChild.data
                    extFlds_lst2.append(extFlds2)
                    extFlds['rtSchPostPrc'] = extFlds_lst2

        if childNode.nodeName == 'rateVersion2':
            for node in childNode.childNodes:
                if node.nodeName == 'rateVersion2List':
                    extFlds3 = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'effectiveDate':
                            extFlds3[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'rateVersionDescription':
                            extFlds3[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'calculationGroup':
                            extFlds3[nd.nodeName] = nd.lastChild.data
                    extFlds_lst3.append(extFlds3)
                    extFlds['rtSchRtVer'] = extFlds_lst3

        if childNode.nodeName == 'ratePreProcessing':
            for node in childNode.childNodes:
                if node.nodeName == 'ratePreProcessingRules':
                    extFlds4 = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'sequence':
                            extFlds4[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'description':
                            extFlds4[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'calculationGroup':
                            extFlds4[nd.nodeName] = nd.lastChild.data
                    extFlds_lst4.append(extFlds4)
                    extFlds['rtSch'] = extFlds_lst4

        if childNode.nodeName == 'rateScheduleBillMsg':
            for node in childNode.childNodes:
                if node.nodeName == 'rateScheduleBillMsgs':
                    extFlds5 = {}
                    for nd in node.childNodes:
                        if nd.nodeName == 'billMessage':
                            extFlds5[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'startDate':
                            extFlds5[nd.nodeName] = nd.lastChild.data
                        if nd.nodeName == 'endDate':
                            extFlds5[nd.nodeName] = nd.lastChild.data
                    extFlds_lst5.append(extFlds5)
                    extFlds['rtSchBillMsg'] = extFlds_lst5
    rateSchedComp[component] = [comnFlds, extFlds]


def getInitiative(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'initiative':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'startDate':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'salesRepresentative':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'isMasterOrSubsidiary':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'mayHaveLeads':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'initiativePrimaryCommunicationChannel':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'canLeadsHaveRep':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'parentInitiative':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'contractOptionParticipationAnalysis':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'statisticsInfo':
            comnFlds[childNode.nodeName] = childNode.childNodes[1].lastChild.data

        if childNode.nodeName == 'initiativeLeadDefinition':
            extFlds1 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'eventSequence':
                    extFlds1[node.nodeName] = node.lastChild.data
                if node.nodeName == 'leadEventType':
                    extFlds1[node.nodeName] = node.lastChild.data
                if node.nodeName == 'daysAfterLeadCreation':
                    extFlds1[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(extFlds1)
            extFlds['initiativeLeadDef'] = extFlds_lst1
    initiativeComp[component] = [comnFlds, extFlds]


def getSalesRep(boDataChildren, component):
    comnFlds = {}
    for childNode in boDataChildren:
        if childNode.nodeName == 'salesRepresentative':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'salesRepresentativeType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
    salesRepComp[component] = [comnFlds]


def getToDoTyp(boDataChildren, component):
    comnFlds = {}
    extFlds = {}
    extFlds_lst1 = []
    extFlds_lst2 = []
    extFlds_lst3 = []
    extFlds_lst4 = []
    extFlds_lst5 = []
    for childNode in boDataChildren:
        if childNode.nodeName == 'toDoType':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'toDoPriority':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'toDoTypeUsage':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'creationProcess':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'messageCategory':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'navigationOption':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'routingProcess':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'description':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'longDescription':
            comnFlds[childNode.nodeName] = childNode.lastChild.data
        if childNode.nodeName == 'messageNumber':
            comnFlds[childNode.nodeName] = childNode.lastChild.data

        if childNode.nodeName == 'toDoTypeRole':
            extFlds1 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'toDoRole':
                    extFlds1[node.nodeName] = node.lastChild.data
                if node.nodeName == 'shouldUseAsDefault':
                    extFlds1[node.nodeName] = node.lastChild.data
            extFlds_lst1.append(extFlds1)
            extFlds['ToDoTypRole'] = extFlds_lst1

        if childNode.nodeName == 'toDoSortKeyType':
            extFlds2 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    extFlds2[node.nodeName] = node.lastChild.data
                if node.nodeName == 'description':
                    extFlds2[node.nodeName] = node.lastChild.data
                if node.nodeName == 'shouldUseAsDefault':
                    extFlds2[node.nodeName] = node.lastChild.data
                if node.nodeName == 'order':
                    extFlds2[node.nodeName] = node.lastChild.data
            extFlds_lst2.append(extFlds2)
            extFlds['ToDoTypSortKey'] = extFlds_lst2

        if childNode.nodeName == 'toDoDrillKeyType':
            extFlds3 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    extFlds3[node.nodeName] = node.lastChild.data
                if node.nodeName == 'table':
                    extFlds3[node.nodeName] = node.lastChild.data
                if node.nodeName == 'field':
                    extFlds3[node.nodeName] = node.lastChild.data
            extFlds_lst3.append(extFlds3)
            extFlds['ToDoTypDrillKey'] = extFlds_lst3

        if childNode.nodeName == 'toDoTypeCharacteristicControl':
            extFlds4 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sortSequence':
                    extFlds4[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicType':
                    extFlds4[node.nodeName] = node.lastChild.data
                if node.nodeName == 'isRequired':
                    extFlds4[node.nodeName] = node.lastChild.data
                if node.nodeName == 'shouldUseAsDefault':
                    extFlds4[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicValue':
                    extFlds4[node.nodeName] = node.lastChild.data
            extFlds_lst4.append(extFlds4)
            extFlds['ToDoTypCharCntl'] = extFlds_lst4

        if childNode.nodeName == 'toDoTypeCharacteristic':
            extFlds5 = {}
            for node in childNode.childNodes:
                if node.nodeName == 'sequence':
                    extFlds5[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicType':
                    extFlds5[node.nodeName] = node.lastChild.data
                if node.nodeName == 'characteristicValue':
                    extFlds5[node.nodeName] = node.lastChild.data
            extFlds_lst5.append(extFlds5)
            extFlds['ToDoTypChar'] = extFlds_lst5
    toDoTypComp[component] = [comnFlds, extFlds]



def init():
    variables_to_clear = [
        schema_dict,
        query,
        bsSchemaDefination,
        boSchemaDefination,
        boLifeCycle,
        final_bo_life_cycle,
        dataArea,
        uiMap,
        batchCntlComp,
        portalComp,
        algorithm,
        algoType,
        algorithmSoftParameter,
        algorithmTypeSoftParameter,
        componentList,
        charType,
        messages_list,
        adjTypeComp,
        featCnfgComp,
        FKRefComp,
        adjTypePrfComp,
        appSvcComp,
        billMsgComp,
        billSegTypComp,
        bktCnfgComp,
        calcLineCatTypComp,
        busFlgTypComp,
        calcGrpComp,
        iwsSvcSOAPComp,
        fieldComp,
        caseTypComp,
        final_case_lfc,
        leadEvntTypComp,
        lookupComp,
        mainObjComp,
        mgmtContentComp,
        migrPlnComp,
        migrReqComp,
        navKeyComp,
        navOptComp,
        ntfTypComp,
        perCntTypComp,
        rateSchedComp,
        initiativeComp,
        salesRepComp,
        toDoTypComp
    ]

    for variable in variables_to_clear:
        variable.clear()