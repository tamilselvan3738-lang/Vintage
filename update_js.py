import os

hamburger_js = """
      // ---------- MOBILE DRAWER ----------
      const mobileHamburger = document.getElementById('mobileHamburger');
      const mobileDrawer = document.getElementById('mobileDrawer');
      const drawerOverlay = document.getElementById('drawerOverlay');
      const closeDrawerBtn = document.getElementById('closeDrawer');
      const mobileDarkToggle = document.getElementById('mobileDarkToggle');
      const mobileRtlToggle = document.getElementById('mobileRtlToggle');
      const mobileLoginBtn = document.getElementById('mobileLoginBtn');
      const home1Option = document.getElementById('home1Option');
      const home2Option = document.getElementById('home2Option');
      const mobileHome1 = document.getElementById('mobileHome1');
      const mobileHome2 = document.getElementById('mobileHome2');

      // mobile toggles
      mobileDarkToggle?.addEventListener('click', () => { 
        const isDark = body.classList.contains('dark');
        if(!isDark) body.classList.add('dark'); else body.classList.remove('dark');
        localStorage.setItem('vinyl_dark', !isDark ? 'true' : 'false');
      });
      mobileRtlToggle?.addEventListener('click', () => { 
        const isRtl = body.classList.contains('rtl');
        if(!isRtl) body.classList.add('rtl'); else body.classList.remove('rtl');
        localStorage.setItem('vinyl_rtl', !isRtl ? 'true' : 'false');
      });
      mobileLoginBtn?.addEventListener('click', () => { window.location.href = './login.html'; });

      home1Option?.addEventListener('click', () => { closeDrawerIfOpen(); });
      home2Option?.addEventListener('click', () => { closeDrawerIfOpen(); });
      mobileHome1?.addEventListener('click', () => { closeDrawerIfOpen(); });
      mobileHome2?.addEventListener('click', () => { closeDrawerIfOpen(); });

      function closeDrawer() {
        if(mobileDrawer) mobileDrawer.classList.remove('open');
        if(drawerOverlay) drawerOverlay.style.display = 'none';
      }
      function closeDrawerIfOpen() {
        if(mobileDrawer?.classList.contains('open')) closeDrawer();
      }
      mobileHamburger?.addEventListener('click', () => {
        if(mobileDrawer) mobileDrawer.classList.add('open');
        if(drawerOverlay) drawerOverlay.style.display = 'block';
      });
      closeDrawerBtn?.addEventListener('click', closeDrawer);
      drawerOverlay?.addEventListener('click', closeDrawer);

      document.querySelectorAll('.mobile-dropdown').forEach(dropdown => {
        const header = dropdown.querySelector('div:first-child');
        header?.addEventListener('click', (e) => {
          e.stopPropagation();
          dropdown.classList.toggle('active');
        });
      });
"""

files_to_update = ["login.html", "registeration.html", "404.html"]

for filename in files_to_update:
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "const mobileHamburger =" not in content:
        insert_idx = content.rfind("})();")
        if insert_idx != -1:
            content = content[:insert_idx] + hamburger_js + "\n      " + content[insert_idx:]
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Injected JS into {filename}")
