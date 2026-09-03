#!/usr/bin/env python3
"""
Emits static redirect stubs for the URLs BookStack used to serve on docs.involvo.io.

docs.involvo.io used to be the wiki; it is now this site. Two kinds of old URL exist:

  * Help pages, whose content moved here    -> redirect to the new page on this site
  * Legal and internal pages, which stayed  -> redirect to wiki.involvo.io

GitHub Pages cannot issue 3xx redirects, so each stub is an HTML page with a canonical
link, a meta refresh and a JS replace. Every stub is noindex, so none of them competes
with the real page in search results.
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, 'public')
WIKI = 'https://wiki.involvo.io'
DOCS = 'https://docs.involvo.io'

# Old BookStack help URLs -> where that content lives now, on this site.
HELP = {
 'start-here/page/what-is-involvo': '/get-started',
 'start-here/page/how-event-information-on-involvo-works': '/get-started/how-involvo-works',
 'start-here/page/do-i-need-an-account': '/get-started/accounts',
 'start-here/page/your-first-event-start-to-finish': '/get-started/your-first-event',
 'start-here/page/what-do-you-want-to-do': '/',
 'start-here': '/get-started',
 'find-opportunities/page/the-feed-and-the-calendar': '/participants/discovering/feed-and-calendar',
 'find-opportunities/page/filters': '/participants/discovering/filters',
 'find-opportunities/page/finding-opportunities-abroad': '/participants/discovering/opportunities-abroad',
 'find-opportunities/page/reading-an-event-page': '/participants/discovering/event-pages',
 'find-opportunities/page/saving-events-and-reminders': '/participants/discovering/saving-events',
 'find-opportunities': '/participants/discovering',
 'take-part/page/how-you-get-into-an-event': '/participants/applying/how-you-get-in',
 'take-part/page/applying-and-what-each-status-means': '/participants/applying/statuses',
 'take-part/page/registering-directly': '/participants/applying/registering-directly',
 'take-part/page/check-in-and-check-out': '/participants/participating/check-in',
 'take-part/page/after-the-event-feedback': '/participants/participating/feedback',
 'take-part/page/when-something-looks-wrong': '/participants/participating/troubleshooting',
 'take-part': '/participants/applying',
 'people/page/seeing-other-attendees': '/participants/people/other-attendees',
 'people/page/how-friend-requests-work': '/participants/people/friend-requests',
 'people/page/your-network-questions': '/participants/people/network-questions',
 'people/page/your-profile-and-qr-code': '/participants/people/profile-and-qr',
 'people/page/what-other-people-can-see-about-you': '/platform/what-others-can-see',
 'people': '/participants/people',
 'publish-manage-events/page/two-ways-an-event-gets-on-involvo': '/organizers/publishing/two-ways',
 'publish-manage-events/page/publishing-your-organizations-event': '/organizers/publishing/publish-your-event',
 'publish-manage-events/page/sharing-an-event-you-found': '/organizers/publishing/share-an-event',
 'publish-manage-events/page/what-moderation-checks': '/platform/moderation',
 'publish-manage-events/page/managing-applications-and-participants': '/organizers/running/applications-and-participants',
 'publish-manage-events/page/check-in-day': '/organizers/running/check-in-day',
 'publish-manage-events/page/feedback-analytics-and-tracking-links': '/organizers/running/feedback-and-analytics',
 'publish-manage-events/chapter/publish-an-event': '/organizers/publishing',
 'publish-manage-events/chapter/manage-an-event': '/organizers/running',
 'publish-manage-events': '/organizers',
 'organizations/page/organization-profiles-and-badges': '/organizations/profiles-and-badges',
 'organizations/page/following-organizations': '/organizations/following',
 'organizations/page/plans-and-limits': '/organizations/plans-and-limits',
 'organizations': '/organizations',
 'account-rewards/page/profile-language-and-location': '/participants/account/profile-and-preferences',
 'account-rewards/page/notifications-email-and-telegram': '/participants/account/notifications',
 'account-rewards/page/impact-points-vs-impact-stars': '/platform/impact-points-and-stars',
 'account-rewards/page/earning-and-spending-stars': '/platform/earning-and-spending-stars',
 'account-rewards/page/referrals-and-daily-rewards': '/platform/referrals-and-rewards',
 'account-rewards': '/participants/account',
}

# Old BookStack URLs whose content stayed on the wiki. Internal-only locations are
# deliberately absent: a public stub naming them would disclose the wiki's internal
# structure for no reader benefit, noindex or not. All six legal pages keep a stub so
# existing bookmarks still resolve, but only privacy-policy and terms-of-service are
# visible to anonymous visitors on the wiki - the other four are restricted there, so
# nothing on this site links to them directly.
WIKI_PATHS = [
 'legal-documentation',
 'legal-documentation/chapter/public',
 'legal-documentation/page/privacy-policy',
 'legal-documentation/page/terms-of-service',
 'legal-documentation/page/cookie-policy',
 'legal-documentation/page/organizer-terms',
 'legal-documentation/page/organizer-dpa',
 'legal-documentation/page/subprocessor-list',
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Moved — INVOLVO</title>
<link rel="canonical" href="{target}">
<meta name="robots" content="noindex, follow">
<meta http-equiv="refresh" content="0; url={target}">
<style>body{{font:16px/1.6 system-ui,sans-serif;margin:12vh auto;max-width:34rem;padding:0 1.25rem;color:#0a0a0a}}a{{color:#0d7ff2}}</style>
</head>
<body>
<h1>This page has moved</h1>
<p>It now lives at <a href="{target}">{target}</a>.</p>
<script>location.replace({target!r})</script>
</body>
</html>
"""


def write(path_parts, target):
    d = os.path.join(PUBLIC, *path_parts)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w') as fh:
        fh.write(TEMPLATE.format(target=target))


def main():
    n = 0
    for old, new in HELP.items():
        write(['books'] + old.split('/'), DOCS + ('' if new == '/' else new))
        n += 1
    for old in WIKI_PATHS:
        write(['books'] + old.split('/'), f'{WIKI}/books/{old}')
        n += 1
    # 'ai-agent-internal-docs' is intentionally not listed: see the note above.
    for shelf in ['involvo-help', 'involvo-legal-compliance']:
        target = DOCS if shelf == 'involvo-help' else f'{WIKI}/shelves/{shelf}'
        write(['shelves', shelf], target)
        n += 1
    print(f'wrote {n} redirect stubs under public/books and public/shelves')


if __name__ == '__main__':
    main()
