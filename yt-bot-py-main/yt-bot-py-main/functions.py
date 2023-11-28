import requests
import time
import json

#url = 'http://10.166.1.98:8112/youtrack'
#timestamp = 1657200000000
#1656617419323


# Конфиг
def read_config():
  file = open('/yt_bot_py/conf/config.json', 'rb')
  conf = json.load(file)
  file.close()
  return conf

def read_time():
    file = open('/yt_bot_py/conf/time.txt', 'r')
    time = file.read()
    file.close()
    return time

def write_file_time(dt):
    file = open('/yt_bot_py/conf/time.txt', 'w')
    file.write(str(dt))
    file.close()

#конвертируем время
def convert_timestamp(timestamp):
    conv_time = time.strftime("%H:%M:%S", time.localtime(int(str(timestamp)[:-3])))
    return conv_time

# Дёрнем из ЮТ все изменения, уз stack
def get_all_activities(url):
  headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer perm:c3RhY2s=.NjEtMTI=.sPh5dDqauqoG4ZqRG8BtrWTutcklEK',
      'Content-Type': 'application/json',
  }
  timestamp = read_time()
  data = {"fields": "id,author(id,name,fullName,login,ringId),timestamp,added(text,name),target(issue(idReadable,id,project(name)),idReadable,project(id,name)),targetMember,field(id,name)","categories":"ArticleCommentAttachmentsCategory,AttachmentRenameCategory,AttachmentVisibilityCategory,AttachmentsCategory,CommentAttachmentsCategory,CommentTextCategory,CommentUsesMarkdownCategory,CommentVisibilityCategory,CommentsCategory,CustomFieldCategory,DescriptionCategory,IssueCreatedCategory,IssueResolvedCategory,IssueUsesMarkdownCategory,IssueVisibilityCategory,LinksCategory,ProjectCategory,SprintCategory,SummaryCategory,TagsCategory,TotalVotesCategory,VcsChangeCategory,VcsChangeStateCategory,VotersCategory,WorkItemCategory", "start": f'{timestamp}', "reverse": "true"} ## ,"start": f'{timestamp}',"$top":50}

 # data = {"fields":"idReadable","query":"in:" + project,"$top":"5000"} # указываем проект и количество задач
  response = requests.get(f'{url}/api/activities', headers=headers, params=data)
  text = response.json()
  dt = int(time.time() * 1000)
  write_file_time(dt)
  return text


# Дёрнем все данные по определённой задаче из ЮТ
def get_data_issue(issue_id,url):
  headers = {
      'Accept': 'application/json',
      'Authorization': 'Bearer perm:c3RhY2s=.NjEtMTI=.sPh5dDqauqoG4ZqRG8BtrWTutcklEK',
      'Content-Type': 'application/json',
  }

  response = requests.get(f'{url}/api/issues/{issue_id}?fields=description,summary,created,reporter(ringId,login,avatarUrl),updated,customFields(projectCustomField(field(name)),value(ringId,id,avatarUrl,buildLink,fullName,isResolved,localizedName,login,minutes,name,presentation,text))', headers=headers,) #params=data)
  return response.json()


# подгонка для Markdown
def rep_i(text):
    text = text.replace(".", "")
    text = text.replace("_", "\_")
    return text

def rep_des(text):
##    text = text.replace("{", "")
#    print(text)
##    text = text.replace("}", "")
#    print(text)
##    text = text.replace("\\n", "\n")
#    print(text)
    #text = text.replace("\\", "")
    #print(text)
##    text = text.replace("[", "\\[")
#    print(text)
##    text = text.replace("'", "")
#    print(text)
    text = text.replace("_","\_")
    text = text.replace("*", "\*")
    text = text.replace("`", "\`")
    text = text.replace('«', '"')
    text = text.replace('»', '"')
#    text = text.replace("$", "\$")
#    text = text.replace("%", "\%")
#    text = text.replace("%", "\%")
#    text = text.replace("^", "\^")
#    text = text.replace("&", "\&")
#    text = text.replace("(", "\(")
#    text = text.replace(")", "\)")

#    text = text.replace("%", "\%")
#    text = text.replace("%", "\%")
#    text = text.replace("%", "\%")
    return text

def rep_sum(text):
    text = text.replace("_","[_]")
#    text = text.replace("-","[-]")
#    text = text.replace(" \ ", " \\ ")
    return text

def rep_description(text):
    text = text.replace("_", "\\_")
    return text
