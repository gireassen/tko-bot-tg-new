import time
import functions
import telebot
import codecs


conf = functions.read_config()
url = conf["youtrack"]["baseUrl"]
project = conf["project"]
bot = telebot.TeleBot(conf["bot"])
chat_id = conf["chat_id"]


all_activities = functions.get_all_activities(url)
#print(all_activities)

issue_list = []
issue_activity = {}
issue_list_author = {}

for i in range(len(all_activities)):
    all = all_activities[i]
    if "issue" in all["target"] and all["target"]["issue"]["project"]["name"] in project:        # == 'Администрирование':
        if all["target"]["issue"]["idReadable"] not in issue_activity and all["$type"] != "IssueCreatedActivityItem":
            issue_activity.update({all["target"]["issue"]["idReadable"]:[]})
            issue_list.append(all["target"]["issue"]["idReadable"])
        if all["$type"] == "CommentActivityItem":
            for b in range(len(all["added"])):
                if "text" in all["added"][b]:
                    added = {"- [[" + functions.convert_timestamp(all["timestamp"]) + "]] #Comments " + (all["added"][b]["text"])[:1500] + ""}
                    issue_list_author.update({all["target"]["issue"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
                    issue_activity[all["target"]["issue"]["idReadable"]].append(added)
        elif all["$type"] == "AttachmentActivityItem":
            for b in range(len(all["added"])):
                if "name" in all["added"][b]:
                    added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #Attachments ' + all["field"]["name"] + ': ' + all["added"][b]["name"] + ''}
                    issue_list_author.update({all["target"]["issue"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
                    issue_activity[all["target"]["issue"]["idReadable"]].append(added)
    elif "project" in all["target"] and all["target"]["project"]["name"] in project:       # == 'Администрирование':
        if all["target"]["idReadable"] not in issue_activity and all["$type"] != "IssueCreatedActivityItem":
            issue_activity.update({all["target"]["idReadable"]:[]})
            issue_list.append(all["target"]["idReadable"])
        if all["$type"] == "IssueCreatedActivityItem":
            issue_id = all["target"]["idReadable"]
            data = functions.get_data_issue(issue_id,url)
            date_create = time.strftime("%d.%m.%Y", time.localtime(int(str(data["updated"])[:-3])))
            summary = data["summary"]
            summary = functions.rep_des(summary)
            link = f'\\[[{issue_id}]({url}/issue/{issue_id})]'
            user_crete = ('#' + data["reporter"]["login"])
            user_crete = functions.rep_i(user_crete)
            user_crete_link = f'\\[[⇗]({url}/users/' + data["reporter"]["ringId"] + ')]'
            assignee = ''
            assignee_link = ''
            for v in range(len(data["customFields"])):
                if data["customFields"][v]["projectCustomField"]["field"]["name"] == "Assignee":
                    assignee = ('#' + data["customFields"][v]["value"]["login"])
                    assignee = functions.rep_i(assignee)
                    assignee_link = f'\\[[⇗]({url}/users/' + data["customFields"][v]["value"]["ringId"] + ')]'
            description = data["description"]
            description = functions.rep_des(description)
            if len(description) > 2000:
                description = (description[:2000] + '...')
            text = f'\\[{date_create}] \U000026A1 {link} {summary} {user_crete}{user_crete_link} \U000026A1 \n- Assignee: {assignee}{assignee_link}\n#Описание: {description}'
            bot.send_message(chat_id, text=text, parse_mode='Markdown') #, reply_markup=keyboard)
        elif all["$type"] == "CustomFieldActivityItem":
            if type(all["added"]) == int:
                added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #CustomField ' + all["field"]["name"] + ': ' + str(all["added"]) + ''}
                issue_list_author.update({all["target"]["idReadable"]: [all["author"]["login"], all["author"]["ringId"]]})
                issue_activity[all["target"]["idReadable"]].append(added)
            else:
                for b in range(len(all["added"])):
                    if "name" in all["added"][b]:
                        added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #CustomField ' + all["field"]["name"] + ': ' + all["added"][b]["name"] + ''}
                        issue_list_author.update({all["target"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
                        issue_activity[all["target"]["idReadable"]].append(added)
        elif all["$type"] == "TextMarkupActivityItem":
            added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #' + all["field"]["id"] + ' ' + all["field"]["name"] + ': ' + all["added"] + ''}
            issue_list_author.update({all["target"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
            issue_activity[all["target"]["idReadable"]].append(added)
        elif all["$type"] == "SimpleValueActivityItem":
            added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #' + all["field"]["id"] + ' ' + all["field"]["name"] + ': ' + all["added"] + ''}
            issue_list_author.update({all["target"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
            issue_activity[all["target"]["idReadable"]].append(added)
        elif all["$type"] == "AttachmentActivityItem":
            for b in range(len(all["added"])):
                if "name" in all["added"][b]:
                    added = {'- [[' + functions.convert_timestamp(all["timestamp"]) + ']] #' + all["field"]["id"] + ' ' + all["field"]["name"] + ': ' + all["added"][b]["name"] + ''}
                    issue_list_author.update({all["target"]["idReadable"]: [all["author"]["login"],all["author"]["ringId"]]})
                    issue_activity[all["target"]["idReadable"]].append(added)


for i in range(len(issue_list)):
    des = ''
    try:
        issue_id = issue_list[i]
        data = functions.get_data_issue(issue_id,url)
        for b in range(len(issue_activity[issue_list[i]])):
            des = des + (str(issue_activity[issue_list[i]][b]))[2:-2] + f'\n'


        date_updated = time.strftime("%d.%m.%Y", time.localtime(int(str(data["updated"])[:-3])))
        summary = data["summary"]
        summary = functions.rep_des(summary)
        link = f'\\[[{issue_id}]({url}/issue/{issue_id})]'
        assignee = ''
        assignee_link = ''
        for v in range(len(data["customFields"])):
            if data["customFields"][v]["projectCustomField"]["field"]["name"] == "Assignee":
                assignee = ('#' + data["customFields"][v]["value"]["login"])
                assignee = functions.rep_i(assignee)
                assignee_link = f'\\[[⇗]({url}/users/' + data["customFields"][v]["value"]["ringId"] + ')]'

        user_update = ('#' + issue_list_author[issue_list[i]][0])
        user_update = functions.rep_i(user_update)
        user_update_link = f'\\[[⇗]({url}/users/' + issue_list_author[issue_list[i]][1] + ')]'



        des = codecs.escape_decode(des)[0].decode('utf8')
        des = functions.rep_des(des)
        text = f'\\[{date_updated}] \U000026A1 {link} {summary} {user_update}{user_update_link} \U000026A1 \n- Assignee: {assignee}{assignee_link} \n{des}'
        bot.send_message(chat_id, text=text, parse_mode='Markdown')  # , reply_markup=keyboard)
    except Exception as err:
        print(err)


