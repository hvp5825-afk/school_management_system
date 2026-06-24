import re

path = r'c:\Users\Harsh\OneDrive\Attachments\Desktop\astniq1\SCHOOL_MANAGEMENT_SYSTEM\authentication\templates\authentication\login.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to replace from the form submit button to the end of the body
pattern = r'(\s*<button type="submit" class="btn-submit">Login to Dashboard</button>\s*</form>)([\s\S]*?)</div>\s*</body>\s*</html>'

new_buttons = r'''\1
        <div style="margin-top: 2rem; border-top: 1px solid #e5e7eb; padding-top: 1.5rem;">
            <p style="text-align: center; color: #6b7280; font-size: 0.875rem; margin-top: 0; margin-bottom: 1rem; font-weight: 500;">Testing the project? Try a demo account:</p>
            <div style="display: flex; gap: 0.5rem; justify-content: space-between;">
                <button type="button" onclick="fillDemo('admin', 'admin123')" style="flex: 1; padding: 0.5rem; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; font-weight: 600; color: #475569; transition: all 0.2s;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f8fafc'">Admin Demo</button>
                <button type="button" onclick="fillDemo('teacher_ramesh12', 'teacher123')" style="flex: 1; padding: 0.5rem; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; font-weight: 600; color: #475569; transition: all 0.2s;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f8fafc'">Teacher Demo</button>
                <button type="button" onclick="fillDemo('aarav307', 'student123')" style="flex: 1; padding: 0.5rem; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 0.375rem; cursor: pointer; font-size: 0.8rem; font-weight: 600; color: #475569; transition: all 0.2s;" onmouseover="this.style.background='#e2e8f0'" onmouseout="this.style.background='#f8fafc'">Student Demo</button>
            </div>
        </div>

        <script>
            function fillDemo(username, password) {
                document.getElementById('username').value = username;
                document.getElementById('password').value = password;
                document.querySelector('form').submit();
            }
        </script>
    </div>
</body>
</html>'''

if re.search(pattern, content):
    content = re.sub(pattern, new_buttons, content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added demo buttons to login.html")
else:
    print("Pattern not found in login.html")
