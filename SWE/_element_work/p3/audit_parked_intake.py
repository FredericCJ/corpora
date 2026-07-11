import json, re
base = r'C:/Users/frede/AppData/Local/Temp/claude/E--dev-corpora/af68f286-e2b9-4227-a910-623820ffa376/scratchpad/'
parked = json.load(open(base + 'p3/parked.json', encoding='utf-8'))['parked']
d = json.load(open(base + 'p3/sweeps/arch-parked-intake.json', encoding='utf-8'))
print('parked count:', len(parked))

def norm(s):
    return re.sub(r'[^a-z0-9]+', '', s.lower())

elnames = set()
for e in d['elements']:
    elnames.add(norm(e['name']))
    elnames.add(norm(e['id']))
    for a in e['aka']:
        elnames.add(norm(a))
rejnames = [norm(r['name']) for r in d['rejected']]

# heads: leading tokens of parked names mapped to admitted element ids or FOLD/DROP markers
head_map = {
    'seda': 'seda', 'halfsynchalfasync': 'half-sync-half-async-arch', 'mapreduce': 'mapreduce',
    'hardwareabstraction': 'hardware-abstraction-layer-arch', 'boardsupportpackage': 'board-support-package',
    'layeredsoftware': 'layered-architecture', 'timetriggered': 'time-triggered-architecture',
    'timespacepartitioning': 'time-space-partitioning', 'eventdrivenarchitecture': 'event-driven-architecture',
    'activeobjectframework': 'FOLD:actor-model-architecture', 'autosarvirtualfunctionbus': 'virtual-function-bus',
    'microkernel': 'microkernel/FOLD', 'bootloader': 'bootloader', 'smallarchitecture': 'DROP',
    'serviceorientedarchitecture': 'service-oriented-architecture', 'twophasecommit': 'two-phase-commit/FOLD',
    'logshipping': 'primary-replica-replication', 'sharednothing': 'shared-nothing-architecture/FOLD',
    'partitioningsharding': 'sharding', 'queryoptimizer': 'FOLD', 'layeredpattern': 'FOLD',
    'fivelayerarchitecture': 'five-layer-architecture', 'channelarchitecture': 'channel-architecture',
    'recursivecontainment': 'recursive-containment', 'hierarchicalcontrol': 'hierarchical-control',
    'virtualmachinepattern': 'virtual-machine-style', 'componentbasedarchitecture': 'component-based-architecture',
    'homogeneousredundancy': 'homogeneous-redundancy', 'triplemodularredundancy': 'triple-modular-redundancy/FOLD',
    'heterogeneousredundancy': 'heterogeneous-redundancy', 'monitoractuator': 'monitor-actuator/FOLD',
    'safetyexecutive': 'safety-executive/FOLD', 'databuspattern': 'data-bus', 'brokerpattern': 'broker',
    'broker': 'broker/FOLD', 'clientserver': 'client-server', 'distributedhashtable': 'distributed-hash-table',
    'sharding': 'FOLD', 'shardingdatapartitioning': 'FOLD', 'distributedreplicatedlog': 'distributed-commit-log',
    'blockchain': 'blockchain', 'searchengineindextier': 'FOLD', 'messagebroker': 'message-broker',
    'messagebus': 'message-bus', 'channeladapter': 'channel-adapter', 'messagingbridge': 'messaging-bridge',
    'pipesandfilters': 'pipes-and-filters/FOLD', 'processmanager': 'process-manager', 'routingslip': 'routing-slip',
    'controlbus': 'control-bus', 'canonicaldatamodel': 'canonical-data-model',
    'guaranteeddelivery': 'guaranteed-delivery', 'durablesubscriber': 'durable-subscriber',
    'datatypechannel': 'datatype-channel', 'integrationstyles': 'file-transfer/shared-db/rpi/messaging (4 admits)',
    'applicationswitching': 'application-switching', 'spatialtemporalpartitioning': 'FOLD',
    'layeredfirmware': 'FOLD', 'redundantchannelstructures': 'FOLD', 'limphome': 'FOLD',
    'dataflowprogramming': 'dataflow-architecture', 'functionasaservice': 'function-as-a-service',
    'modelviewcontroller': 'model-view-controller/FOLD', 'publishsubscribe': 'publish-subscribe-style',
    'abstractionlayer': 'FOLD', 'selfcontainedcomponent': 'self-contained-component',
    'authoritativeserver': 'authoritative-server/FOLD', 'layeredgameengine': 'game-engine-layered-architecture',
    'serverconcurrencymodels': 'thread-per-connection + prefork-server', 'kernelbypass': 'kernel-bypass',
    'splittophalf': 'DROP', 'compilationpipeline': 'compiler-pipeline', 'protocollayering': 'protocol-layering',
    'interfacedefinitionlanguage': 'interface-definition-language', 'modelview': 'mv-family',
    'frontcontroller': 'front-controller/FOLD', 'pagecontroller': 'page-controller/FOLD',
    'templateview': 'template-view/FOLD', 'transformview': 'transform-view/FOLD', 'twostepview': 'two-step-view',
    'applicationcontroller': 'application-controller/FOLD', 'transactionscript': 'transaction-script',
    'domainmodel': 'domain-model/FOLD', 'tablemodule': 'table-module', 'servicelayer': 'service-layer',
    'remotefacade': 'remote-facade', 'clientsessionstate': 'client-session-state',
    'serversessionstate': 'server-session-state', 'databasesessionstate': 'database-session-state',
    'boundedcontext': 'bounded-context/FOLD', 'contextmap': 'context-map',
    'anticorruptionlayer': 'anticorruption-layer', 'cqrs': 'cqrs', 'eventsourcing': 'event-sourcing-style/FOLD',
    'layers': 'FOLD', 'blackboard': 'blackboard/FOLD', 'presentationabstractioncontrol': 'presentation-abstraction-control/FOLD',
    'reflection': 'reflection-architecture', 'domainobject': 'domain-object', 'sharedrepository': 'shared-repository',
    'messagechannel': 'message-channel', 'messageendpoint': 'message-endpoint',
    'messagetranslator': 'message-translator', 'messagerouter': 'message-router', 'clientproxy': 'client-proxy',
    'requestor': 'requestor', 'invoker': 'invoker', 'clientrequesthandler': 'client-request-handler',
    'serverrequesthandler': 'server-request-handler', 'replicatedcomponentgroup': 'replicated-component-group',
    'container': 'component-container', 'activator': 'activator', 'firewallproxy': 'FOLD',
    'authorization': 'authorization', 'failover': 'failover', 'redundancy': 'redundancy',
    'unitsofmitigation': 'units-of-mitigation', 'errorcontainmentbarrier': 'error-containment-barrier',
    'someoneincharge': 'someone-in-charge', 'faultobserver': 'fault-observer', 'systemmonitor': 'system-monitor',
    'maintenanceinterface': 'maintenance-interface', 'healthcheck': 'health-check-api/FOLD',
    'decouplingmiddleware': 'FOLD', 'gracefuldegradation': 'graceful-degradation/FOLD',
    'processpairs': 'process-pairs', 'saga': 'saga/FOLD', 'shedworkatperiphery': 'DROP',
    'presentationmodel': 'presentation-model', 'flux': 'flux', 'elmarchitecture': 'elm-architecture',
    'unidirectionaldataflow': 'FOLD', 'islandsarchitecture': 'islands-architecture', 'sidecar': 'sidecar',
    'ambassador': 'ambassador', 'gatewayaggregation': 'gateway-aggregation/-routing/-offloading (3 admits)',
    'backendsforfrontends': 'backends-for-frontends', 'gatekeeper': 'gatekeeper', 'stranglerfig': 'strangler-fig',
    'queuebasedloadleveling': 'queue-based-load-leveling', 'competingconsumers': 'competing-consumers-arch',
    'publishersubscriber': 'FOLD', 'scheduleragentsupervisor': 'scheduler-agent-supervisor',
    'leaderelection': 'leader-election', 'deploymentstamps': 'deployment-stamps + geode',
    'federatedidentity': 'federated-identity + valet-key', 'healthendpointmonitoring': 'FOLD',
    'staticcontenthosting': 'static-content-hosting + external-configuration-store',
    'claimcheck': 'sequential-convoy/async-request-reply/choreography admits + claim-check DROP + messaging-bridge FOLD',
    'computeresourceconsolidation': 'compute-resource-consolidation',
    'indextable': 'index-table + materialized-view', 'halfobject': 'half-object-plus-protocol-arch',
    'transactionaloutbox': 'transactional-outbox', 'safetytacticscatalog': 'DROP',
    'hlaruntimeinfrastructure': 'hla-federated-simulation', 'mvfamily': 'FOLD',
    'privilegeseparation': 'privilege-separation', 'sandbox': 'process-sandboxing',
    'securechannel': 'secure-channel', 'singlesignon': 'single-sign-on',
    'demilitarizedzone': 'demilitarized-zone + packet-filter-firewall + proxy-based-firewall',
    'policydecisionpoint': 'policy-decision-point', 'intrusiondetectionsystem': 'intrusion-detection-system',
    'secretsmanagement': 'secrets-management', 'defenseindepth': 'defense-in-depth',
    'recursivecontrol': 'recursive-control', 'bodyguard': 'bodyguard', 'objectsynchronizer': 'object-synchronizer',
    'singleaccesspoint': 'DROP', 'dynamicobjectmodel': 'adaptive-object-model', 'chainedprocessors': 'chained-processors',
    'eventcollaboration': 'event-collaboration', 'reportingdatabase': 'reporting-database',
    'polyglotpersistence': 'polyglot-persistence', 'distributedsnapshot': 'distributed-snapshot',
    'sessionstateplacementtrio': 'FOLD (members admitted)',
}

uncovered = []
for p in parked:
    n = norm(p['name'])
    hit = None
    for h, v in head_map.items():
        if n.startswith(h):
            hit = v
            break
    if hit is None and (n in elnames or any(r == n for r in rejnames)):
        hit = 'name-match'
    if hit is None:
        uncovered.append(p['name'] + '  [' + p['scout'] + ']')
print('uncovered:', len(uncovered))
for u in uncovered:
    print(' -', u)
