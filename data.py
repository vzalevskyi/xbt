__author__ = 'vitalii.zalevskyi'


frames = {
    #=====Frames=====

    "loginFrame" : "login",
    "appFrame" : "appframe",
    "mailBoxFrame" : "MailboxFrame",
    "navigationFrame" : "navigation",


}
user_data = {
    #====Controls=====
    #"url" : "http://test-webforms-ui-a.hosted-commerce.net/wfds/",
    "url" : "https://portal.hosted-commerce.net/sps/",
    "username" : "connect1",
    "password" : "connect1",

#    "username" : "cewuduty",
#    "password" : "pinide2",

}

xpth = {
    #=====Frames=====
    "loginFrame" : "//iframe[@name='login']",
    "appFrame" : "//iframe[@id='appframe']",
    "mailBoxFrame" : "//frame[@name='MailboxFrame']",
    "navigationFrame" : "//frame[@name='navigation']",

    #====Controls=====
    "username" : "//input[@id='username']",
    "password" : "//input[@id='password']",
    "submit" : "//input[@id='submit']",
    "wfLink" : "//a[@href='/portal/webforms.jsp']/span",
    "nextStepsArrow" : "//div[@class='nextStepsArrow']",
    "sentFolder" : "//*[@id='SENT']/a",
    "draftsFolder" : "//*[@id='DRAFTS']/a"

}
