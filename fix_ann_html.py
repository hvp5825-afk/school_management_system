import os
import re

with open('authentication/templates/authentication/teacher_dashboard.html', 'r', encoding='utf-8') as f:
    dashboard_html = f.read()

# Extract everything up to <div class="container">
match = re.search(r'(.*?)<div class="container">', dashboard_html, re.DOTALL)
if not match:
    print("Failed to find container start")
    exit(1)

head_and_sidebar = match.group(1)
# Make sure the title is right
head_and_sidebar = head_and_sidebar.replace('<title>Teacher Dashboard</title>', '<title>Announcements | Teacher Panel</title>')

with open('authentication/templates/authentication/teacher_announcements.html', 'r', encoding='utf-8') as f:
    ann_html = f.read()

# Extract the <style> block and the <div class="premium-wrapper"> from ann_html
style_match = re.search(r'<style>(.*?)</style>', ann_html, re.DOTALL)
premium_match = re.search(r'<div class="premium-wrapper">(.*?)</div>\s*{% endblock %}', ann_html, re.DOTALL)

if not style_match or not premium_match:
    print("Failed to parse ann_html")
    exit(1)

style_content = style_match.group(1)
premium_content = premium_match.group(1)

final_html = head_and_sidebar + """
<style>
""" + style_content + """
</style>

<div class="container">
    {% if messages %}
        {% for message in messages %}
            <div class="alert" style="padding: 1rem; background: #d1fae5; color: #065f46; border-radius: 0.5rem; margin-bottom: 1rem;">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}

    <div class="premium-wrapper">
        """ + premium_content + """
    </div>
</div>
</main>
</body>
</html>
"""

with open('authentication/templates/authentication/teacher_announcements.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Fixed teacher_announcements.html")
