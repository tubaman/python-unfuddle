# Python API for Unfuddle

Here's a python wrapper around the Unfuddle API.

## Example

```python
from unfuddle import Unfuddle

unf = Unfuddle(account, username, password)

report_title = "My Active Tickets"
reports = unf.get_ticket_reports()
my_active_tickets_report, = [r for r in reports if report_title in r['title']]
report = unf.generate_ticket_report(my_active_tickets_report['id'])
for group in report['groups']:
    print group['title']
    for t in group['tickets'][:5]:
        print "%s %s" % (t['number'], t['summary'])
    print
```

For more examples, take a look at the tests.
