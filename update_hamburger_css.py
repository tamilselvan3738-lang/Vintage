import os
import re

def update_css():
    folder = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(folder, "index.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        index_content = f.read()

    # Extract CSS from index.html
    css_start_marker = "/* MOBILE / TABLET (<= 1280px) */"
    css_end_marker = "/* ==========================================================================\n       HOME PAGE:"
    
    css_start = index_content.find(css_start_marker)
    css_end = index_content.find(css_end_marker)
    
    if css_start == -1 or css_end == -1:
        print("CSS markers not found in index.html")
        return
        
    extracted_css = index_content[css_start:css_end]
    
    print("Extracted CSS length:", len(extracted_css))

    for filename in os.listdir(folder):
        if filename.endswith(".html") and filename != "index.html":
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find where to insert or replace in other files
            s_start = content.find("/* MOBILE / TABLET (<= 1280px) */")
            if s_start != -1:
                s_end = content.find("/* ==========================================================================", s_start)
                if s_end == -1:
                    s_end = content.find("/* ========== UNIVERSAL RESPONSIVE BREAKPOINTS", s_start)
                if s_end == -1:
                    s_end = content.find("</style>", s_start)
                
                if s_end != -1:
                    content = content[:s_start] + extracted_css + "\n    " + content[s_end:]
                    print(f"Replaced CSS in {filename}")
            else:
                # If not present, just insert before /* ========== UNIVERSAL RESPONSIVE BREAKPOINTS or </style>
                insert_pos = content.find("/* ========== UNIVERSAL RESPONSIVE BREAKPOINTS")
                if insert_pos == -1:
                    insert_pos = content.find("/* ==========================================================================")
                if insert_pos == -1:
                    insert_pos = content.find("</style>")
                
                if insert_pos != -1:
                    content = content[:insert_pos] + extracted_css + "\n    " + content[insert_pos:]
                    print(f"Inserted CSS in {filename}")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    update_css()
