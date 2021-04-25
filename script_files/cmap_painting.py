import sys
import os
import random
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from jinja2 import Template



def script_path():
    '''set current path, to script path'''
    current_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(current_path)
    return current_path
    
    
def write_file(filename, text, mode='w'):
    '''write to file'''
    try:
        with open(filename, mode, encoding='utf-8') as f:
            f.write(text)
            
    except Exception as err:
        print('failed to write to file: {}, err: {}'.format(filename, err))
        
    return None
    
    
def cmap_colors_list():
    '''list of cmap colors'''
    cmap_colors_str = '''Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r,
        CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r,
        OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r,
        Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r,
        PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r,
        RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r,
        Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r,
        YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r,
        bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r,
        coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r,
        gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r,
        gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r,
        hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r,
        ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r,
        seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r,
        tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r,
        viridis, viridis_r, winter, winter_r'''
    cmap_colors = [item.strip() for item in cmap_colors_str.split(',') if item.strip()]
    # ~ cmap_colors = cmap_colors[:10]
    return cmap_colors
    
    
if __name__ == "__main__":
    script_path()
    
    
    # ****** data set ******
    cmap_colors = cmap_colors_list()
    data = [list(range(0, 101, 5))]*len(cmap_colors)
    df = pd.DataFrame(data)
    df = df.transpose()
    df.columns = cmap_colors
    
    vertical = True
    if vertical:
        df = df.transpose()
        
        
    # ****** apply style to dataframe ******
    styled = df.style
    for index, color in enumerate(cmap_colors):
        print(index, color)
        if vertical:
            styled.background_gradient(axis=1, subset=([color],), cmap=color)
        else:
            styled.background_gradient(axis=0, subset=[color], cmap=color)
            
            
    # ****** style table ******
    styled = styled.set_table_styles([
        {
        # '' - to whole table
        'selector': '',
        'props': [
            ('margin-left', 'auto'),
            ('margin-right', 'auto'),
            ('width', '100%'),
            ]
        },
        {
        'selector': 'td',
        'props': [
            ('border', '1px solid #ddd'),
            ('border-spacing', '20px'),
            ('padding', '15px'),
            ('width', '5%'),
            ]
        }
        ])
        
        
    # ****** write to html ******
    template = Template('''
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    
    <body style="margin: 0;">
        <header style="background-color: lightblue;width: 100%;height:100%;padding-top: 10px;">
            <h1 style="text-align: center;">Pandas DataFrame</h1>
            <h3 style="text-align: center;">background_gradient cmap</h3>
            <hr>
        </header>
        
        <main>
            <div style="margin: 0 auto;width: 60%;border: 0px solid green;padding: 0px;">
            {{main_table}}
            </div>
        </main>
        
        <footer style="background-color: lightblue;width: 100%;height:100%;padding-bottom: 10px;">
            <hr>
            <h3 style="text-align: center;"><a href="https://github.com/streanger">streanger [github]</a></h3>
            <h3 style="text-align: center;"><a href="https://pypi.org/user/stranger/">stranger [pypi]</a></h3>
        </footer>
    </body>
</html>
''')

    df_html = styled.render()
    rendered = template.render(main_table=df_html)
    if vertical:
        html_file = 'cmap_colors_vertical.html'
    else:
        html_file = 'cmap_colors_horizontal.html'
    write_file(html_file, rendered)
    print(f'data saved to: {html_file}')
    
    
'''
apply gradient to rows:
    https://stackoverflow.com/questions/61524844/how-to-style-transposed-multiindex-dataframe
    subset=(rows,)
    subset=([0,1,2],)
    
'''
