import os

def update_all_html():
    folder = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(folder, "index.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Extract button
    btn_start = index_content.find("<!-- Mobile Hamburger -->")
    if btn_start == -1:
        print("Button not found in index.html")
        return
    btn_end = index_content.find("</nav>", btn_start)
    button_html = index_content[btn_start:btn_end]

    # Extract drawer
    drawer_start = index_content.find("<!-- mobile drawer -->")
    if drawer_start == -1:
        print("Drawer not found in index.html")
        return
    drawer_end = index_content.find("<!-- ===", drawer_start)
    if drawer_end == -1:
        drawer_end = index_content.find("<!--", drawer_start + 20)
    drawer_html = index_content[drawer_start:drawer_end]

    print("Extracted button length:", len(button_html))
    print("Extracted drawer length:", len(drawer_html))

    for filename in os.listdir(folder):
        if filename.endswith(".html") and filename != "index.html":
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Replace button
            b_s = content.find("<!-- Mobile Hamburger -->")
            if b_s != -1:
                b_e = content.find("</nav>", b_s)
                if b_e != -1:
                    content = content[:b_s] + button_html + content[b_e:]
            
            # Replace drawer
            d_s = content.find("<!-- mobile drawer -->")
            if d_s != -1:
                d_e = content.find("<!-- ===", d_s)
                if d_e == -1:
                    d_e = content.find("<section", d_s)
                if d_e != -1:
                    # To keep spacing nice, find the start of the next section
                    while d_e > d_s and content[d_e-1] in ' \n\r\t':
                        d_e -= 1
                    content = content[:d_s] + drawer_html.strip() + "\n\n" + content[d_e:]
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {filename}")

if __name__ == "__main__":
    update_all_html()
