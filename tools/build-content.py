#!/usr/bin/env python3
"""
Generates content/**.mdx from the INVOLVO Help pages held in BookStack.

This is a one-off migration aid, not a sync: it was run once to seed the site,
and the MDX in content/ is the source of truth from here on. It rewrites the
wiki's internal /books/... links to this site's routes, repoints screenshots at
public/screenshots, and attaches per-page SEO front matter.
"""
import json, os, re, sys

# Directory of BookStack page JSON dumps (one <page-id>.json per page, as returned by
# GET /api/pages/<id>). Point BOOKSTACK_DUMP at your own export to re-run this.
SRC = os.environ.get('BOOKSTACK_DUMP', './.bookstack-dump')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content')

# BookStack page id -> (target path, sidebar/page title, meta description)
PAGES = {
 34: ('get-started/index', 'What is INVOLVO',
      'INVOLVO is where events and opportunities for young people in Moldova are published, found and joined — by participants and by the organizations running them.'),
 36: ('get-started/how-involvo-works', 'How INVOLVO works',
      'Some events are maintained by the organization running them, others are added by someone who found them. Knowing which you are looking at explains most of what you see.'),
 35: ('get-started/accounts', 'Do I need an account?',
      'What you can do on INVOLVO without signing in, and which features — applying, saving events, check-in and networking — need an account.'),
 37: ('get-started/your-first-event', 'Your first event, start to finish',
      'The whole path from finding an event on INVOLVO to turning up and checking in, in the order it actually happens.'),

 40: ('participants/discovering/feed-and-calendar', 'The feed and the calendar',
      'Two ways to browse what is on INVOLVO: a feed you scroll and sort, and a month calendar for when your question is about a particular date.'),
 41: ('participants/discovering/filters', 'Filters',
      'Narrow the feed and the calendar by topic, place, date, online-only and open registration, and combine as many filters as you like.'),
 42: ('participants/discovering/opportunities-abroad', 'Finding opportunities abroad',
      'The Mobility filter shows events held in another country that are open to people applying from yours — youth exchanges, training courses and similar programs.'),
 43: ('participants/discovering/event-pages', 'Reading an event page',
      'What an INVOLVO event page tells you: the organizer links, the details that appear once you are interested, and what the event status means.'),
 44: ('participants/discovering/saving-events', 'Saving events and reminders',
      'Save an event to find it again, then set a reminder — for the event itself and for the registration deadline that actually costs people places.'),

 46: ('participants/applying/how-you-get-in', 'How you get into an event',
      'Some events ask you to apply and be selected, some let you register directly, and some send you to the organizer’s own form. How to tell which.'),
 47: ('participants/applying/statuses', 'Applying, and what each status means',
      'Applications are decided first, then your place is confirmed by you. Every status in both stages, and the one you have to act on.'),
 48: ('participants/applying/registering-directly', 'Registering directly',
      'Registering for an event that takes people without a selection step, including registering as a guest without an account.'),

 49: ('participants/participating/check-in', 'Check in and check out',
      'Checking in records that you came — it is what the organizer counts and what unlocks the list of other people at the event.'),
 50: ('participants/participating/feedback', 'After the event: feedback',
      'The feedback organizers ask for after an event, who sees it, and what it is used for.'),
 51: ('participants/participating/troubleshooting', 'When something looks wrong',
      'What to do when an event page, your application status, a check-in or an email does not look the way you expect.'),

 53: ('participants/people/other-attendees', 'Seeing other attendees',
      'Every event has a networking view listing the people who checked in — who can see it, what it shows about you, and how to get on it.'),
 54: ('participants/people/friend-requests', 'How friend requests work',
      'Friend requests on INVOLVO go through the other person’s network questions, with a limited number of attempts. What that means from both sides.'),
 55: ('participants/people/network-questions', 'Your network questions',
      'The five questions someone must answer correctly before they can send you a friend request — choosing them, changing them, and what changing them does not do.'),
 56: ('participants/people/profile-and-qr', 'Your profile and QR code',
      'Your profile is what someone sees when they look you up. Share it in person with your QR code or your profile link.'),

 71: ('participants/account/profile-and-preferences', 'Profile, language and location',
      'Your name and picture, the city you are shown events for, the interface language, and the languages you can attend events in.'),
 72: ('participants/account/notifications', 'Notifications: email and Telegram',
      'What INVOLVO sends you, on which channel, and how to change or switch off each kind of notification.'),

 59: ('organizers/publishing/two-ways', 'Two ways an event gets on INVOLVO',
      'An event is either published by the organization running it, or added by somebody who found it. The two paths behave differently.'),
 62: ('organizers/publishing/publish-your-event', 'Publishing your organization’s event',
      'Setting up an event as the organization running it: the basics, when and where, visibility, links, and the registration choice that matters most.'),
 60: ('organizers/publishing/share-an-event', 'Sharing an event you found',
      'Adding an event your organization is not running, what review it goes through, and what happens to it afterwards.'),

 63: ('organizers/running/applications-and-participants', 'Managing applications and participants',
      'Approve, reject or waitlist applications, then get the people you accepted to confirm — and watch the group that never answered.'),
 64: ('organizers/running/check-in-day', 'Check-in day',
      'Running check-in on the day: the QR code, checking people in yourself, location checks, and the practical advice that keeps a queue moving.'),
 65: ('organizers/running/feedback-and-analytics', 'Feedback, analytics and tracking links',
      'What you can see after an event: attendance, feedback and where your registrations came from, using tracking links.'),

 67: ('organizations/profiles-and-badges', 'Organization profiles and badges',
      'What an organization profile shows on INVOLVO, and what the badges on it mean.'),
 68: ('organizations/following', 'Following organizations',
      'Following an organization on INVOLVO, what it changes in your feed, and what the organization can send you.'),
 69: ('organizations/plans-and-limits', 'Plans and limits',
      'The limits that apply to an organization on INVOLVO — participants per event, messaging, and what a plan changes.'),

 57: ('platform/what-others-can-see', 'What other people can see about you',
      'Exactly what other attendees, your friends, organizers and anonymous visitors can see about you on INVOLVO.'),
 61: ('platform/moderation', 'What moderation checks',
      'Events added by someone other than the organizer go through review before they appear. What that review looks at.'),
 73: ('platform/impact-points-and-stars', 'Impact Points vs Impact Stars',
      'INVOLVO has two separate things that sound alike: Impact Points, which measure activity, and Impact Stars, which you spend.'),
 74: ('platform/earning-and-spending-stars', 'Earning and spending Impact Stars',
      'How Impact Stars are earned by taking part rather than paid for, and what they can be spent on.'),
 75: ('platform/referrals-and-rewards', 'Referrals and daily rewards',
      'Inviting somebody to INVOLVO with your referral code, and the rewards you can claim just for showing up.'),
}

# BookStack route -> this site's route
LINKS = {
 '/books/start-here/page/what-is-involvo': '/get-started',
 '/books/start-here/page/do-i-need-an-account': '/get-started/accounts',
 '/books/start-here/page/how-event-information-on-involvo-works': '/get-started/how-involvo-works',
 '/books/start-here/page/your-first-event-start-to-finish': '/get-started/your-first-event',
 '/books/find-opportunities': '/participants/discovering',
 '/books/find-opportunities/page/the-feed-and-the-calendar': '/participants/discovering/feed-and-calendar',
 '/books/find-opportunities/page/filters': '/participants/discovering/filters',
 '/books/find-opportunities/page/finding-opportunities-abroad': '/participants/discovering/opportunities-abroad',
 '/books/find-opportunities/page/reading-an-event-page': '/participants/discovering/event-pages',
 '/books/find-opportunities/page/saving-events-and-reminders': '/participants/discovering/saving-events',
 '/books/take-part': '/participants/applying',
 '/books/take-part/page/how-you-get-into-an-event': '/participants/applying/how-you-get-in',
 '/books/take-part/page/applying-and-what-each-status-means': '/participants/applying/statuses',
 '/books/take-part/page/registering-directly': '/participants/applying/registering-directly',
 '/books/take-part/page/check-in-and-check-out': '/participants/participating/check-in',
 '/books/take-part/page/after-the-event-feedback': '/participants/participating/feedback',
 '/books/take-part/page/when-something-looks-wrong': '/participants/participating/troubleshooting',
 '/books/people': '/participants/people',
 '/books/people/page/seeing-other-attendees': '/participants/people/other-attendees',
 '/books/people/page/how-friend-requests-work': '/participants/people/friend-requests',
 '/books/people/page/your-network-questions': '/participants/people/network-questions',
 '/books/people/page/your-profile-and-qr-code': '/participants/people/profile-and-qr',
 '/books/people/page/what-other-people-can-see-about-you': '/platform/what-others-can-see',
 '/books/publish-manage-events': '/organizers',
 '/books/publish-manage-events/page/two-ways-an-event-gets-on-involvo': '/organizers/publishing/two-ways',
 '/books/publish-manage-events/page/sharing-an-event-you-found': '/organizers/publishing/share-an-event',
 '/books/publish-manage-events/page/what-moderation-checks': '/platform/moderation',
 '/books/publish-manage-events/page/publishing-your-organizations-event': '/organizers/publishing/publish-your-event',
 '/books/publish-manage-events/page/managing-applications-and-participants': '/organizers/running/applications-and-participants',
 '/books/publish-manage-events/page/check-in-day': '/organizers/running/check-in-day',
 '/books/publish-manage-events/page/feedback-analytics-and-tracking-links': '/organizers/running/feedback-and-analytics',
 '/books/organizations/page/organization-profiles-and-badges': '/organizations/profiles-and-badges',
 '/books/organizations/page/following-organizations': '/organizations/following',
 '/books/organizations/page/plans-and-limits': '/organizations/plans-and-limits',
 '/books/account-rewards': '/participants/account',
 '/books/account-rewards/page/profile-language-and-location': '/participants/account/profile-and-preferences',
 '/books/account-rewards/page/notifications-email-and-telegram': '/participants/account/notifications',
 '/books/account-rewards/page/impact-points-vs-impact-stars': '/platform/impact-points-and-stars',
 '/books/account-rewards/page/earning-and-spending-stars': '/platform/earning-and-spending-stars',
 '/books/account-rewards/page/referrals-and-daily-rewards': '/platform/referrals-and-rewards',
}

IMG = re.compile(r'https://docs\.involvo\.io/uploads/images/gallery/2026-09/([^)\s]+\.png)')
LINK = re.compile(r'\]\((/books/[^)]+)\)')


def transform(md: str) -> str:
    md = IMG.sub(lambda m: '/screenshots/' + m.group(1), md)

    def sub_link(m):
        target = m.group(1)
        if target not in LINKS:
            raise SystemExit(f'unmapped link: {target}')
        return '](' + LINKS[target] + ')'

    md = LINK.sub(sub_link, md)
    # The wiki says "Involvo"; the product's own branding is INVOLVO.
    md = re.sub(r'\bInvolvo\b', 'INVOLVO', md)
    return md.strip() + '\n'


def yaml_escape(s: str) -> str:
    return s.replace('"', '\\"')


def main():
    written = 0
    for pid, (path, title, desc) in PAGES.items():
        src = json.load(open(f'{SRC}/{pid}.json'))
        body = transform(src.get('markdown') or '')
        target = os.path.join(OUT, path + '.mdx')
        os.makedirs(os.path.dirname(target), exist_ok=True)
        front = (
            '---\n'
            f'title: "{yaml_escape(title)}"\n'
            f'description: "{yaml_escape(desc)}"\n'
            # No "last updated" line - this is documentation, not a wiki page history.
            'theme:\n  timestamp: false\n'
            '---\n\n'
        )
        with open(target, 'w') as fh:
            fh.write(front + f'# {title}\n\n' + body)
        written += 1
    print(f'wrote {written} pages')


if __name__ == '__main__':
    main()
