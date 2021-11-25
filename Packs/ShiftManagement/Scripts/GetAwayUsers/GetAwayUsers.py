import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

from typing import Dict, Any
import traceback

''' MAIN FUNCTION '''


def main():
    try:
        users_command_response: Dict = demisto.executeCommand("getUsers", {})
        if is_error(users_command_response) or not users_command_response:
            raise DemistoException(f'Could not retrieve users\nError details: {get_error(users_command_response)}')
        users_info: List[Dict] = users_command_response[0]['Contents']
        away_users = [user for user in users_info if user.get('isAway', False)]
        print(away_users)
        return_results(CommandResults(
            outputs_key_field='id',
            outputs_prefix='CortexXSOAR.AwayUsers',
            readable_output=tableToMarkdown('Away Users', away_users,
                                            headers=['username', 'email', 'name', 'phone', 'roles', 'isAway'],
                                            headerTransform=string_to_table_header, removeNull=True),
            outputs=away_users
        ))
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute GetAwayUsers. Error: {str(e)}')


''' ENTRY POINT '''

if __name__ in ('__main__', '__builtin__', 'builtins'):
    with open('./test_data/away_user', 'w') as f:
        f.write('{"accUser": false, "addedSharedDashboards": ["health-status-dashboard", "Cost Optimization Instances", "Threat Intelligence Feeds", "Troubleshooting Instances", "my-home-dashboard", "sla-dashboard", "097e5436-d8f0-49b7-a19d-a05c60ed1039", "Cost Optimization Playbooks", "My Threat Landscape", "Troubleshooting Playbooks"], "allRoles": ["Administrator"], "dashboards": null, "dateFormat": "", "defaultAdmin": true, "disableHyperSearch": false, "disabled": false, "editorStyle": "", "email": "", "helpSnippetDisabled": false, "homepage": "", "hours24": "", "id": "admin", "image": "232698060###user_image_admin.png", "investigationPage": "", "isAway": true, "lastLogin": "2021-11-25T07:02:57.149388523Z", "lastLoginMaster": "0001-01-01T00:00:00Z", "name": "Admin", "notificationsSettings": {"email": {"all": true}, "pushNotifications": {"all": true}}, "phone": "+650-123456", "playgroundCleared": false, "playgroundId": "d4f55b55-db35-430e-81ab-49edc550675f", "preferences": {"automationSearchValuePreference": "AssignAnalystToIncidentOOODEV", "automationTypeFilterPreference": "All", "cartState": {"selectedDependencies": [], "selectedPackId": null, "versionToInstall": ""}, "integrationsCategoryFilter": null, "integrationsDeprecatedFilter": null, "integrationsSearchValue": null, "integrationsTypeFilter": null, "userPreferencesDashboardsOrder": ["my-home-dashboard", "My Threat Landscape", "health-status-dashboard", "sla-dashboard", "Troubleshooting Playbooks", "097e5436-d8f0-49b7-a19d-a05c60ed1039", "Cost Optimization Playbooks", "Troubleshooting Instances", "Threat Intelligence Feeds", "Cost Optimization Instances"], "userPreferencesDefaultDashboard": "my-home-dashboard", "userPreferencesIncidentTable": [{"isDefault": true, "key": "id", "position": 0, "width": 110}, {"isDefault": true, "key": "name", "position": 2, "width": 300}, {"isDefault": true, "key": "type", "position": 3, "width": 200}, {"isDefault": true, "key": "severity", "position": 4, "width": 80}, {"isDefault": true, "key": "status", "position": 5, "width": 80}, {"isDefault": true, "key": "owner", "position": 6, "width": 160}, {"isDefault": true, "key": "roles", "position": 7, "width": 160}, {"isDefault": true, "key": "playbookId", "position": 8, "width": 150}, {"isDefault": true, "key": "occurred", "position": 9, "width": 200}, {"isDefault": true, "key": "dueDate", "position": 10, "width": 200}], "userPreferencesIncidentTableQueries": {"Open Jobs in the last 7 days": {"picker": {"predefinedRange": {"id": "7", "name": "Last 7 days"}}, "query": "-status:closed category:job"}, "Open incidents in the last 7 days": {"isDefault": true, "picker": {"predefinedRange": {"id": "7", "name": "Last 7 days"}}, "query": "-status:closed -category:job"}}, "userPreferencesIndicatorsTable": [{"isDefault": true, "key": "indicator_type", "position": 1, "width": 120}, {"isDefault": true, "key": "value", "position": 2, "width": 300}, {"isDefault": true, "key": "score", "position": 4, "width": 120}, {"isDefault": true, "key": "firstSeen", "position": 5, "width": 275}, {"isDefault": true, "key": "lastSeen", "position": 6, "width": 275}, {"isDefault": true, "key": "timestamp", "position": 8, "width": 190}, {"isDefault": true, "key": "relatedIncCount", "position": 9, "width": 150}, {"isDefault": true, "key": "sourceBrands", "position": 12, "width": 175}, {"isDefault": true, "key": "sourceInstances", "position": 13, "width": 175}, {"isDefault": true, "key": "expirationStatus", "position": 14, "width": 175}, {"isDefault": true, "key": "expiration", "position": 15, "width": 190}, {"isDefault": true, "key": "isUnit42Enriched", "notSortable": true, "position": 100, "width": 250}], "userPreferencesSawPluginToast": true, "userPreferencesShowDeprecatedAF": "F", "userPreferencesShowDisabledAF": "F", "userPreferencesUseDefaultDashboardsPerRole": true, "userPreferencesWarRoomFilter": {"categories": ["chats", "incidentInfo", "commandAndResults", "notes"], "fromTime": "0001-01-01T00:00:00Z", "pageSize": 0, "tagsAndOperator": false, "usersAndOperator": false}, "userPreferencesWarRoomFilterExpanded": false, "userPreferencesWarRoomFilterMap": {"Chats only": {"categories": ["chats"], "fromTime": "0001-01-01T00:00:00Z", "pageSize": 0, "tagsAndOperator": false, "usersAndOperator": false}, "Default Filter": {"categories": ["chats", "incidentInfo", "commandAndResults", "notes"], "fromTime": "0001-01-01T00:00:00Z", "pageSize": 0, "tagsAndOperator": false, "usersAndOperator": false}, "Playbook results": {"categories": ["playbookTaskResult", "playbookErrors", "justFound"], "fromTime": "0001-01-01T00:00:00Z", "pageSize": 0, "tagsAndOperator": false, "usersAndOperator": false}}, "userPreferencesWarRoomFilterOpen": true, "userPreferencesWelcomePopupUnit42IntelSeen": true}, "readOnly": false, "roles": {"demisto": ["Administrator"]}, "shortcutsDisabled": false, "theme": "", "timeFormat": "", "timeZone": "", "type": 0, "userTimeZone": "", "username": "admin", "wasAssigned": false}')
    main()
