import re
import os

sidebar_path = 'd:/BANGJEJE.DEV/CMS/admin/src/partials/sidebar.html'
style_path = 'd:/BANGJEJE.DEV/CMS/admin/src/css/style.css'

with open(sidebar_path, 'r', encoding='utf-8') as f:
    content = f.read()

nav_start = content.find('<nav')
nav_end = content.find('</nav>') + len('</nav>')
if nav_start != -1 and nav_end != -1:
    new_nav = '''<nav x-data="{selected: $persist('Dashboard')}">
      <div>
        <h3 class="mb-4 text-xs uppercase leading-[20px] text-gray-400">
          <span class="menu-group-title" :class="sidebarToggle ? 'lg:hidden' : ''">Dashboard</span>
        </h3>
        <ul class="flex flex-col gap-4 mb-6">
          <li>
            <a href="index.html" @click="selected = 'Dashboard'" class="menu-item group" :class="selected === 'Dashboard' ? 'menu-item-active' : 'menu-item-inactive'">
              <span class="menu-item-text">Overview</span>
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h3 class="mb-4 text-xs uppercase leading-[20px] text-gray-400">
          <span class="menu-group-title" :class="sidebarToggle ? 'lg:hidden' : ''">CONTENT</span>
        </h3>
        <ul class="flex flex-col gap-4 mb-6">
          <li>
            <a href="articles.html" @click="selected = 'Articles'" class="menu-item group" :class="selected === 'Articles' ? 'menu-item-active' : 'menu-item-inactive'">
              <span class="menu-item-text">Articles</span>
            </a>
          </li>
          <li>
            <a href="case-studies.html" @click="selected = 'Case Studies'" class="menu-item group" :class="selected === 'Case Studies' ? 'menu-item-active' : 'menu-item-inactive'">
              <span class="menu-item-text">Case Studies</span>
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h3 class="mb-4 text-xs uppercase leading-[20px] text-gray-400">
          <span class="menu-group-title" :class="sidebarToggle ? 'lg:hidden' : ''">RESOURCES</span>
        </h3>
        <ul class="flex flex-col gap-4 mb-6">
          <li>
            <a href="digital-assets.html" @click="selected = 'Digital Assets'" class="menu-item group" :class="selected === 'Digital Assets' ? 'menu-item-active' : 'menu-item-inactive'">
              <span class="menu-item-text">Digital Assets</span>
            </a>
          </li>
        </ul>
      </div>
    </nav>'''
    
    # We also need to add "View Website" and "Logout" at the bottom of the sidebar.
    # We can just put it after the <nav> block
    
    extra = '''
    <div class="mt-auto pb-4">
      <ul class="flex flex-col gap-4">
        <li>
          <a href="https://bangjeje.dev" target="_blank" class="menu-item group menu-item-inactive">
            <span class="menu-item-text">View Website</span>
          </a>
        </li>
        <li>
          <a href="#" class="menu-item group menu-item-inactive">
            <span class="menu-item-text">Logout</span>
          </a>
        </li>
      </ul>
    </div>
    '''
    
    content = content[:nav_start] + new_nav + extra + content[nav_end:]
    with open(sidebar_path, 'w', encoding='utf-8') as f:
        f.write(content)

with open(style_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace brand colors to #9929EA palette roughly.
# #9929EA is our 500 color.
css = re.sub(r'--color-brand-500: #465fff;', '--color-brand-500: #9929EA;', css)
css = re.sub(r'--color-brand-600: #3641f5;', '--color-brand-600: #7b1dbd;', css)
css = re.sub(r'--color-brand-700: #2a31d8;', '--color-brand-700: #621796;', css)

with open(style_path, 'w', encoding='utf-8') as f:
    f.write(css)
