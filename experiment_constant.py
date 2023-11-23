import os

WEB2URL={
    'amazon': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/amazon2018/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/amazon2020/index.html"
    },
    'twitch': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/twitch2019/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/twitch2020/index.html"
    },
    'w3c':{
        'oldurl':"file:///Users/wzz/Desktop/webProject/w3schools2016/index.html",
        'newurl':"file:///Users/wzz/Desktop/webProject/w3schools2019/index.html"
    },
    'walmart': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/walmart2018/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/walmart2020/index.html"
    },
    'ebay': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/ebay2019/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/ebay2022/index.html"
    },
    'office': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/office2018/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/office2020/index.html"
    },
    'msn': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/msn2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/msn2021/index.html"
    },
    'yahoo': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/yahoo2020/Yahoo.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/yahoo2022/Yahoo.html"
    },
    'microsoft': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/microsoft2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/microsoft2022/index.html"
    },
    'weather': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/weather2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/weather2022/index.html"
    },
    'booking': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/booking2018/index.en-gb.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/booking2020/index.en-gb.html"
    },
    'chase': {
        'oldurl': "http://1.117.174.176/chase2021/",
        'newurl': "http://1.117.174.176/chase2022/"
    },
    'cdc': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/cdc2018/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/cdc2022/index.html"
    },
    'healthline': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/healthline2021/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/healthline2022/index.html"
    },
    'Uber': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/Uber2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/Uber2022/index.html"
    },
    'Youtube': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/Youtube2018/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/Youtube2020/index.html"
    },
    'LinkedIn': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/linkedin2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/linkedin2021/index.html"
    },
    'tripadvisor': {
        'oldurl': "http://1.117.174.176/tripadvisor2019/",
        'newurl': "http://1.117.174.176/tripadvisor2022/"
    },
    'Fandom': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/fandom2020/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/fandom2022/index.html"
    },
    'paypal': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/paypal2021/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/paypal2022/index.html"
    },
    'allrecipes': {
        'oldurl': "file:///Users/wzz/Desktop/webProject/allrecipes2019/index.html",
        'newurl': "file:///Users/wzz/Desktop/webProject/allrecipes2022/index.html"
    },
}
# WEB2SCRIPT={
#     'weather': [
#         'weather3'
#     ],
#     'booking': [
#         'booking'
#     ],
#     'Youtube' : [
#         'Youtube1'
#     ],
#     'Fandom' : [
#         'Fandom'
#     ],
#     'paypal' : [
#         'paypal2'
#     ],
# }

WEB2SCRIPT={
    'amazon': [
        'amazon_cart','amazon_home','amazon_searchdropdown','amazon_searchinput',
        'amazon_searchinput2'
    ],
    'twitch': [
        'twitch_liulan', 'twitch_login', 'twitch_more', 'twitch_more2',
        'twitch_search', 'twitch_search2', 'twitch_signin', 'twitch_signin2', 'twitch_user'
    ],
    'w3c':[
        'w3c1', 'w3c2', 'w3c3', 'w3c4', 'w3c5', 'w3c6', 'w3c7', 'w3c_certification', 'w3c_like', 'w3c_tutorial'
    ],
    'walmart': [
        'walmart_account', 'walmart_cart', 'walmart_dropdown', 'walmart_enteremail', 'walmart_feedback', 'walmart_home'
        , 'walmart_menu', 'walmart_searchbutton', 'walmart_searchinput', 'walmart_signup', 'walmart_youtube'
    ],
    'ebay': [
        'ebay_cart', 'ebay_notify', 'ebay_pause',
        'ebay_search', 'ebay_searchinput'
    ],
    'office': [
        'office', 'office2', 'office3', 'office_product'
    ],
    'msn': [
        'msn', 'msn2'
    ],
    'yahoo': [
        'yahoo_mail', 'yahoo_notification', 'yahoo_search', 'yahoo_searchinput', 'yahoo_signin', 'yahoo_signin2'
    ],
    'microsoft': [
        'microsoft', 'microsoft2', 'microsoft_search'
    ],
    'weather': [
        'weather', 'weather2', 'weather3'
    ],
    'booking': [
        'booking', 'booking2'
    ],
    'chase': [
        'chase', 'chase2'
    ],
    'cdc': [
        'cdc', 'cdc2', 'cdc_rss'
    ],
    'healthline': [
        'healthline', 'healthline2'
    ],
    'Uber': [
        'Uber', 'Uber2'
    ],
    'Youtube': [
        'Youtube1', 'Youtube2', 'Youtube3', 'Youtube_browse', 'Youtube_browse2', 'Youtube_help', 'Youtube_help2',
        'Youtube_history', 'Youtube_history2', 'Youtube_searchinput'
    ],
    'LinkedIn': [
        'LinkedIn', 'LinkedIn2'
    ],
    'tripadvisor': [
        'tripadvisor', 'tripadvisor2', 'tripadvisor3'
    ],
    'Fandom': [
        'Fandom', 'Fandom2', 'Fandom3'
    ],
    'paypal': [
        'paypal', 'paypal2'
    ],
    # 'allrecipes': [
    #     'allrecipes', 'allrecipes2', 'allrecipes3'
    # ],
}
