from datetime import datetime
from mailwizz_funcs.setup import setup
from mailwizz.endpoint.campaigns import Campaigns
from data.config import TEST_LIST_ID, KAZAN_LIST_ID

setup()

endpoint = Campaigns()

NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
DATE_TEMPLATE = 'mailwizz_funcs/dates_template.html'


def create_campaign(subject, name='auto_mailings', send_at=NOW, list_uid=TEST_LIST_ID, template=DATE_TEMPLATE):
    
    response = endpoint.create({
        'name': name,
        'type': 'regular',
        'from_name': 'TEZ TOUR Казань',
        'from_email': 'kazan@tez-tour.com',
        'subject': subject,  # required
        'reply_to': 'kazan@tez-tour.com',  # required
        'send_at':NOW ,
        # required, this will use the timezone which customer selected
        'list_uid': TEST_LIST_ID,  # required
        # 'segment_uid'   : 'SEGMENT-UNIQUE-ID',# optional, only to narrow down

        'options': {
        'url_tracking': 'yes',  # yes | no
        'json_feed': 'no',  # yes | no
        'xml_feed': 'no',  # yes | no
        'plain_text_email': 'yes',  # yes | no
        'email_stats': 'kazan@tez-tour.com',  # a valid email address where we should send the stats after campaign done

        # - if autoresponder uncomment bellow:
        # 'autoresponder_event'            : 'AFTER-SUBSCRIBE', # AFTER-SUBSCRIBE or AFTER-CAMPAIGN-OPEN
        # 'autoresponder_time_unit'        : 'hour', # minute, hour, day, week, month, year
        # 'autoresponder_time_value'       : 1, # 1 hour after event
        # 'autoresponder_open_campaign_id' : 1, # INT id of campaign, only if event is AFTER-CAMPAIGN-OPEN,

        # - if this campaign is advanced recurring, you can set a cron job style frequency.
        # - please note that this applies only for regular campaigns.
        # 'cronjob'         : '0 0 * * *', # once a day
        # 'cronjob_enabled' : 1, # 1 or 0
    },
        'template': {
        'content': template,
        # 'template_uid': 'TEMPLATE_UID',
        # 'content'         : open('template-example.html', 'rb').read(),
        'inline_css': 'yes',  # yes | no
        # 'plain_text'      : None, # leave empty to auto generate
        'auto_plain_text': 'yes',  # yes | no
    },

    })

    
    print(response.content)