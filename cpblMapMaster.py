#./usr/bin/python
# -*- coding: latin-1 -*-

"""

2014: colorize_svg() is the latest function to fill in colours according to data in an svg geographic map, created from SHP files, typically (see our convert_to_svg.py).



 # # # # Comments below are old and scattered.


Sept 2011: okay, working to use AlexSchultz's program to make a tool., svgcountrymap()

Sept 2010: Oh, revolution. People are using an SVG map of the world with tagged regions and then using beautifulsoup to simply insert colours into the data, by country. unbelievably fast and simple! Forget plotting.
Pick any of these...
http://commons.wikimedia.org/wiki/Category:Blank_SVG_maps_of_the_world
See AlexSchultz's stuff (I've downloaded it all in GIS/)


Sept 2010: Situation similar...?

polipoly: someone made a nice few tools for working with US geo codes of various kinds.

Someone Aug 2010 says:  The country data basemap 
uses are lines, not polygons. You will have to find another (shapefile?) 
dataset that provides country polygons for the countries you are 
interested in. 



--------------------------------
Sept 2009: Another attempt at getting this junk to work osgeo is able to read my shapefile, but I don't knwo what coordinates it's in and I can't move it over to basemap to plot with it. 
 Basemap's interface is very nice. You can set an area threshold ie resolution, which makes plotting reallly fast.

The basemap demo below works well. (but only on csrv; no basemap on cpbl).

(I think I gave up and switched to QGIS or something, didn't I???)
"""


import os
from cpblUtilities import tonumeric, tsvToDict
from copy import deepcopy
from codecs import open
import numpy as np
import matplotlib as mpl
import pandas as pd
import scipy

def rgb_to_hex(rgb,nanval='#080808'):
    """
what about mpl.colors.rgb2hex? (okay, but it doesn't deal with nan's. maybe that's good; I sould de-nan things before calling rgb2hex...)

    """
    if np.isnan(rgb[0]):
        return(nanval)
    if len(rgb)==4:
        rgb=(rgb[0]*rgb[3],   rgb[1]*rgb[3],  rgb[2]*rgb[3])
    return '#%02x%02x%02x' %tuple(np.array(rgb)*255.0)

                


def demoBetterDirectLoadSHAPE():
    import shpUtils
    ss=shpUtils.loadShapefile('/home/cpbl/rdc/inputData/healthRegions/shp/HR000b07_PZ.shp')
    return(ss['features'])
    # now do whatever you want with the resulting data
    # i'm going to just print out the first feature in this shapefile
    print shpRecords[0]['dbf_data']
    for part in shpRecords[0]['shp_data']:
        print part, shpRecords[0]['shp_data'][part]

import pylab as plt
#import matplotlib.pyplot as plt


def try_osgeo():
    try:
      from osgeo import ogr
    except:
      import ogr




    import re
    import os
    import cpblUtilities
    reload(cpblUtilities)
    from cpblUtilities import unique, doSystem,tsvToDict
    from cpblUtilitiesMathGraph import  tonumeric, overplotLinFit,xTicksLogIncome
    from copy import deepcopy
    import cpblDefaults
    reload(cpblDefaults)
    defaults=cpblDefaults.defaults()
    import cpblStata
    reload(cpblStata)
    #from cpblStata import *
    #from pylab import *
    import pylab





    from matplotlib.mlab import prctile_rank
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap as Basemap

    # cities colored by population rank.

    m = Basemap()

    #following fails: no epxlanation. grrrrrrrrrrr!
    shp_info = m.readshapefile(defaults['inputPath']+'healthRegions/shp/test','HRuid')
    #woeiur Following fails: needs conversion by mapproj??
    shp_info = m.readshapefile(defaults['inputPath']+'healthRegions/shp/HR000b07_PZ','HRuid')
    woeiur
    shp_info = m.readshapefile('/home/cpbl/tmp/cities','cities')
    x, y = zip(*m.cities)
    pop = []
    for item in m.cities_info:
        population = item['POPULATION']
        if population < 0: continue # population missing
        pop.append(population)
    popranks = prctile_rank(pop,100)
    colors = []
    for rank in popranks:
        colors.append(plt.cm.jet(float(rank)/100.))
    m.drawcoastlines()
    m.fillcontinents()
    m.scatter(x,y,25,colors,marker='o',edgecolors='none',zorder=10)
    plt.title('City Locations colored by Population Rank')
    plt.show()





def _demo_colorize_svg():
    import re
    import random
    blanksvgfile='/home/cpbl/bin/GIS/AlexSchultz/countriesCPBL.svg'
    ff=codecs.open(blanksvgfile,'r','utf8').read()
    cc=np.unique(re.findall('id="(..)"',ff,re.DOTALL))
    regions2datavalues=pd.Series(dict([[ac,random.random()] for ac in cc]))
    colorize_svg(regions2datavalues,blanksvgfile,outfilename='__tmp_svgcol_tmp.svg',cmap=None,addcolorbar=True,ylabel=None,colorbarlimits=None)

    blanksvgfile='/home/projects/sprawl2/okai/input/svgmaps/'*0+'USA_Counties_with_FIPS_and_names.svg' # Need to make a copy of this and put it in bin/GIS!
    #os.system('google-chrome '+blanksvgfile+'&')
    cc=np.unique(re.findall('id="(.....)"',open(blanksvgfile,'r').read(),re.DOTALL))

    regions2datavalues=pd.Series(dict([[ac,3*random.random()-1] for ac in cc]))
    colorize_svg(regions2datavalues,blanksvgfile,outfilename='tmptmp2.svg',cmap=None,addcolorbar=True,ylabel=None,colorbarlimits=None)


    from cpblUtilities import biLinearColorscale
    thecmap,thelookup,dummy=biLinearColorscale([],regions2datavalues.values,0.0,noplot=True, mapname='twotwo')
    colorize_svg(regions2datavalues,blanksvgfile,outfilename='tmptmp3.svg',cmap='twotwo',addcolorbar=thelookup,ylabel=None,colorbarlimits=None)
    #os.system('google-chrome tmptmp2.svg&')
    #os.system('google-chrome tmptmp3.svg&')

    #  END OF DEMO MODE
    return


def colorize_svg(geo2data_or_color=None, blanksvgfile=None,outfilename=None,data2color=None,addcolorbar=None,cbylabel=None,
                 demo=False,scratchpath=None,customfeatures=None,colorbarlimits=None,testingRaiseSVGs=False, hideElementsWithoutData=False):
    """
    hideElementsWithoutData uses visible:none to get rid (with least computation in rendering) all elements that do not have a data value.

    2014Dec: Add a javascript hook in these, now, to make them zoomable inside a web viewing portal.
    """
    if demo:
        _demo_colorize_svg()
        return
    assert addcolorbar in [False,True,None] # Ensure the call is for this new version. Alternatively, default to True, and simply ignore it when it's not appropriate.
    if scratchpath is None:
        try:
            from cpblDefaults import paths
            scratchpath=paths['scratch']
        except(ValueError) as e:
            scratchpath = './____tmp_'# if scratchpath is None else os.path.split(outfilename)[0]+'/____tmp_'

    import codecs # Never use built-in open anymore
    if colorbarlimits is None:
        colorbarlimits=[-np.inf, np.inf]

    def check_if_numeric(a): # Tell a float or numpy float from  arrays, strings
       try:
           float(a)
       except (ValueError,TypeError) as e: 
           return False
       return True
    def isdec(cc):
                return(cc.isdigit() or cc in '.')

    def _defaultCustomFeatures(ablanksvgfile):
        # Hard code some parameters here for the format of the map
        # (and, if relevant, the placement of the colorbar) These
        # serve as examples for how to construct the customfeatures
        # dict.
        if os.path.split(ablanksvgfile)[1] in ['USA_Counties_with_FIPS_and_names.svg',]:
            CF=dict(cbarpar=dict(expandx=1.2, movebartox=540,movebartoy=80,scalebar=0.75),
            groupsare='path',
            path_style = """font-size:12px;fill-rule:nonzero;stroke:#FFFFFF;stroke-opacity:1;stroke-width:0.1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:""",
            )

        elif os.path.split(ablanksvgfile)[1] in ['countriesCPBL.svg']:
            CF=dict(cbarpar=dict(expandx=1, movebartox=540,movebartoy=80,scalebar=0.75),
            path_style="""1;stroke:#ffffff;stroke-width:0.99986994;stroke-miterlimit:3.97446823;stroke-dasharray:none;stroke-opacity:1;fill:""",
            groupsare='g',
            )
        else:
            raise("do_not_know_that_map")
        return(CF)


    def _hexcolors_into_svg(_geo2hex,svgtext,customfeatures,   hideElementsWithoutData= None ):
        #assert egvalue.__class__ in [str] # Check that we have a hex-color lookup table!
        #assert cmap is None # It doesn't make sense to pass a cmap if we've given an explicit colour lookup
        ####import csv

        assert len(_geo2hex) == len(_geo2hex.index.unique()) # No duplicate data to colour entries

        from BeautifulSoup import BeautifulSoup
        # Load into Beautiful Soup
        soup = BeautifulSoup(svgtext, selfClosingTags=['defs','sodipodi:namedview'])
        # Find geographic groups
        paths = soup.findAll(CF['groupsare'])

        # Color the counties based on the index and value of _geo2hex (pandas series)
        for p in paths:
            if p['id'] not in ["State_Lines", "separator"]:
                try:
                    dval=_geo2hex[p['id']]  
                    assert isinstance(dval,str)
                    p['style'] = CF['path_style'] +dval
                except KeyError:
                    if  hideElementsWithoutData:         #What if I want to hide those without 
                        p['style'] = 'display: none'
                    continue

        return( soup.prettify())

    # The blank svg info could be passed as a string rather than a filename:
    assert blanksvgfile is not None
    if '\n' in blanksvgfile or len(blanksvgfile)>1000:
        svg=blanksvgfile
    else:
        svg = codecs.open(blanksvgfile, 'r','utf8').read()


    if svg is not None:
        if customfeatures is None:
            print(' You passed SVG code, rather than a filename, to colorize_svg. We will use our best guess for how to interpret it and where to place a colorbar. Use the customfeatures flag to specify more behaviour.')
        CF=dict(cbarpar=  dict(expandx=1.2, movebartox=540,movebartoy=80,scalebar=0.75), 
        groupsare='path',
        path_style = """fill:""",
        )
    else:
        CF=_defaultCustomFeatures(blanksvgfile)
    if customfeatures is not None:
        CF.update(customfeatures)
    cbarpar=CF['cbarpar']
    egvalue=geo2data_or_color.values[0]

    geo2dataWerePassed = check_if_numeric(egvalue)
    if geo2dataWerePassed:
        geo2data=geo2data_or_color
        assert len(geo2data) == len(geo2data.index.unique()) # No duplicate data to colour entries
    else:
        geo2color=geo2data_or_color


    from cpblUtilities import linearColormapLookup
    # I think here I assume geo2data are a pandas Series?

    # Determine geo2color:
    import scipy
    if geo2dataWerePassed and data2color.__class__ is scipy.interpolate.interpolate.interp1d:
        geo2color=geo2data.map(data2color)
    elif geo2dataWerePassed and data2color.__class__ is str: #Implies linear map of cmap of given name
        cmap=data2color
        data2color=linearColormapLookup(cmap,geo2data_or_color.values)
        geo2color=geo2data.map(data2color)
    elif geo2dataWerePassed and data2color.__class__ is pd.Series:
        ConvolveHere
    else:
        fooo
    assert geo2color is not None
    geo2hexcolor=geo2color.map(lambda zx: rgb_to_hex(tuple(zx)))
    

    # Fill the svg:
    svgfilled=_hexcolors_into_svg(geo2hexcolor,svg,CF  ,hideElementsWithoutData= hideElementsWithoutData)
    # We shouldn't need to save it, in general, until we've added the colorbar. But: [[ 2014Jan: Saving as file is only needed for TX and CA (!) state bg maps, at the moment, but do it anyway, for all. For some reason, sg.fromfile works but not sg.fromstring on those two maps.  (I reuse the temporary file below, anyway.)
                # Until Dec 2013, I used svgutils, and could pass the map without colorbar as a text string. But does svg_stack allow that? For now, create a temporary file]]
   #    filledMapfilename=
    if geo2dataWerePassed and addcolorbar is None:
        addcolorbar is True


    # Add a javascript tool for web zooming:
    import re
    svgfilled=re.sub('(<svg.*?>)',r'\1'+"""\n   <script xlink:href="/js/SVGPan.js"/> \n  """,svgfilled)

    if addcolorbar is False and outfilename is not None:
        with codecs.open(outfilename,'w','utf8') as f: 
            f.write(svgfilled)
        if testingRaiseSVGs:
            os.system('google-chrome '+outfilename)
        return
    if outfilename is not None:
        filledMapfilename=scratchpath+os.path.split(outfilename)[1]+'-tmpFilled.svg'
        with codecs.open(filledMapfilename,'w','utf8') as f: 
            f.write(svgfilled)

    # Determine enough information to draw a colorbar:

    """
    if geo2dataWerePassed:#  We've been passed a lookup of data values, not of colour values
        # So, if addcolorbar is True and colormapping is None, we should assume and devise a linear colormap correspondence; if colormapping is
        # instead a mapping from data values (NOT regions!) to color values, we use it. 
        # In either case, it's possible to specify the base colormap as cmap.
        # In the case when it's a mapping, it could be as an interp1 function or an explicit lookup (dict or pandas Series)
        #####rm:        # When implementing the non-linear colormap /custom case,   I would just check here for the extra argument.
        if cmap is None:
            cmap='hot'
        #if colorbreak is not None:
        #fig,colourLookup,=plot_biLinearColorscale([[0.4,0.0,0.0],[1.0,1.0,.9],[0.0,0.4,0.0]],[min(countryValues),max(countryValues)])
        from cpblUtilities import linearColormapLookup
        from scipy import interpolate #scipy.interpolate.
        if addcolorbar.__class__  in [interpolate.interp1d] or addcolorbar.__class__ in [dict,pd.Series]: #Backwards compatibility: This is the value for colormapping
            assert colormapping is None
            colormapping=addcolorbar
            addcolorbar=True
        if colormapping.__class__  in [interpolate.interp1d]: #Backwards compatibility: This is the value for colormapping
            region2colours=geo2data_or_color.map(colormapping)
###            data2colorinterp=linearColormapLookup(cmap,geo2data_or_color.values)
            data2colorlookup=dict([[zz,colormapping(zz)] for zz in geo2data_or_color.values])
        #elif addcolorbar.__class__  in [pd.core.series.Series]:
        #    data2colorlookup=addcolorbar.to_dict()
        #elif addcolorbar.__class__  in [dict]:
        #    data2colorlookup=addcolorbar
        elif colormapping.__class__ in [dict,pd.Series]:
            data2colorinterp=linearColormapLookup(cmap,geo2data_or_color.values)
            region2colours=geo2data_or_color.map(data2colorinterp)
            data2colorlookup=addcolorbar
        elif addcolorbar in [None,False,True]:
            data2colorinterp=linearColormapLookup(cmap,geo2data_or_color.values)
            region2colours=geo2data_or_color.map(data2colorinterp)
        else:
            uhhhhWhatIsregion2colours
    """
    if 1:
        if addcolorbar:
            """ Add a colorbar. However, there are various possibilities for how; see above.
            """
            ####if addcolorbar.__class__ in [pd.Series]:
            #from lxml import etree
            assert outfilename is not None
            import svgutils.transform as sg
            import sys 
            CBfilename=scratchpath+os.path.split(outfilename)[1]+'-tmpCB.svg'
            ### csvgout=colorize_svg(region2colours,cmap=cmap,blanksvgfile=blanksvgfile,colorbarlimits=colorbarlimits)


            if 0:
                from lxml import etree
                xxx=etree.parse(svgout)
                oiuoiuuuuuuuuuuuuuuu

                base_svg=sg.fromstring(svgout)
            base_svg=sg.fromfile(filledMapfilename)
            ww,hh=base_svg.get_size() # This is sometimes just numbers, but sometimes there are units too (px).
            unitsSuffix=''
            if 1:#any(not isdec(cc) for cc in ww): # What to do when there are units? .. .isdigit()
                # Assume measure is digits then units:
                ww,unitsSuffix=''.join([cc  for cc in ww if isdec(cc)]),''.join([cc  for cc in ww if not isdec(cc)])  
                hh,unitsSuffix2=''.join([cc  for cc in hh if isdec(cc)]),''.join([cc  for cc in hh if not isdec(cc)])
                assert unitsSuffix==unitsSuffix2
            plt.figure(6354)
            hax=plt.gca()
            from cpblUtilities import addColorbarNonImage

            # First, deal with case (Jul2014, of most importance) with explicit color mapping in data2color
            if data2color is not None:
                if data2color.__class__ is scipy.interpolate.interpolate.interp1d:
                    allD=sorted(np.unique(geo2data.values))
                    # Shouldn't this include the limits, if they're specified??
                    d2c=dict([[aa,data2color(aa)] for aa in allD+colorbarlimits if np.isfinite(aa) and  aa>=colorbarlimits[0] and aa <= colorbarlimits[1]])
                    # We're getting  :  [(0.0, array([ nan,  nan,  nan])), (0.0078125, array([ nan,  nan,  nan])), 
                    
                    assert not any([np.isnan(aa[0]) for aa in d2c.values()])
                    """
                    df=pd.DataFrame(geo2data)
                    df.color=
                    sorted(np.unique(geo2data.values)).map(data2color)
                    d2c=geo2dict([[aa,bb] for aa,bb in  data2colorlookup.items() if not any(np.isnan(bb)) and aa>=colorbarlimits[0] and aa<=colorbarlimits[1]])
                    """
                #hbax=addColorbarNonimage(d2c,useaxis=None,ylabel=cbylabel)
                hbax=addColorbarNonImage(d2c,ylabel=cbylabel)#data2color=None,data=None,datarange=None,cmap=None,useaxis=None,ylabel=None,colorbarfilename=None,location=None,ticks=None):


            """
            if addcolorbar and data2color is None:
                hbax=addColorbarNonimage(geo2data_or_color.min(),geo2data_or_color.max(),useaxis=None,ylabel=ylabel,cmap=cmap)
            else: # Use custom/nonlinear colorbar data values stretching..
                #get finite valued colours only:
                d2c=dict([[aa,bb] for aa,bb in data2colorlookup.items() if not any(np.isnan(bb)) and aa>=colorbarlimits[0] and aa<=colorbarlimits[1]])

                if addcolorbar:
                    hbax=addColorbarNonimage(d2c,useaxis=None,ylabel=ylabel)
            """

            plt.setp(hax,'visible',False)
            hbax.ax.set_aspect(6)
            plt.savefig(CBfilename, bbox_inches='tight', pad_inches=0.1)

            if cbarpar['movebartox']=='auto':
                assert cbarpar['movebartoy']=='auto'

                # Try new method with svg_stack rather than svgutils:
                import svg_stack as ss

                doc = ss.Document()

                A='____tmp_tmppart1.svg'
                B='../okai/scratch/analysisTIGERcountiesMap_delta12_fourway.svg-tmpCB.svg'
                C='trash/red_ball.svg'
                layout1 = ss.HBoxLayout()
                layout1.addSVG(filledMapfilename,alignment=ss.AlignTop|ss.AlignHCenter)
                layout1.addSVG(CBfilename,alignment=ss.AlignCenter)#,stretch=0.5)

    #layout2 = ss.VBoxLayout()

    #layout2.addSVG(C,alignment=ss.AlignCenter)
    #layout2.addSVG(C,alignment=ss.AlignCenter)
    #layout2.addSVG(C,alignment=ss.AlignCenter)
    #layout1.addLayout(layout2)

                doc.setLayout(layout1)
                print(' Saving (auto mode in cbarpar) '+outfilename)
                doc.save(outfilename)


            else: # Use cbarpar values
                # get the plot objects from constituent figures.
                cbsvg=sg.fromfile(CBfilename)
                svg1,svg2 = base_svg.getroot(),cbsvg.getroot()
                if cbarpar['movebartox']=='auto':
                    assert cbarpar['movebartoy']=='auto'
                    # Below is old debug code working on using more automated fatures of svgutils. I switched to svg_stack, above, instead.
                    impoosible_to_get_here
                    cbw,cbh=cbsvg.get_size()


                    from svgutils.transform import from_mpl
                    from svgutils.templates import VerticalLayout,ColumnLayout

                    ###svg = fromfile('../tests/circle.svg')
                    layout = VerticalLayout#ColumnLayout(2)
                    layout.add_figure(base_svg)
                    layout.add_figure(cbsvg)

                    layout.save('stack_svg.svg')
                    oiuoiu
                    layout = VerticalLayout()

                    fig1 = plt.figure()
                    plt.plot([1,2])
                    fig2 = plt.figure()
                    plt.plot([2,1])

                    layout.add_figure(from_mpl(fig1))
                    layout.add_figure(from_mpl(fig2))

                    print from_mpl(fig1).get_size()
                    layout.save('stack_plots.svg')

                    fofoiu
                svg2.moveto(cbarpar['movebartox'],cbarpar['movebartoy'], scale=cbarpar['scalebar'])

                #create new SVG figure
                fsvg = sg.SVGFigure(str(float(ww)*cbarpar['expandx'])+unitsSuffix,hh)
                #fsvg.save(outfilename+'__nothing.svg')

                # append plots and labels to figure
                fsvg.append([svg1, svg2])
                # save generated SVG files
                fsvg.save(outfilename)
            plt.close(6354)
            return
        elif addcolorbar is False:
            return(colorize_svg(region2colours,cmap=cmap,blanksvgfile=blanksvgfile,outfilename=outfilename,addcolorbar=addcolorbar,colorbarlimits=colorbarlimits))
        else:
            unhandledStophere
    elif egvalue.__class__ in [np.ndarray]:#  We got an RGB lookup table
        assert addcolorbar is False # we cannot put a scale on a colorbar if we don't know the data values.
        assert colormapping is None
        if cmap is not None:
            print('Whaaaaaaaaaaaaaa is cmap doing here?')
            cmap=None
        #assert cmap is None # It doesn't make sense to pass a cmap if we've given an explicit colour lookup
        #assert hexcolorlookup is None and cmap is None
        hexlookup=geo2data_or_color.map(lambda zx: rgb_to_hex(tuple(zx)))

        return(colorize_svg(hexlookup,cmap=cmap,blanksvgfile=blanksvgfile,outfilename=outfilename,colorbarlimits=colorbarlimits))









########################################################################################
################################################################################################
################################################################################################
if __name__ == '__main__':
################################################################################################
################################################################################################
################################################################################################
################################################################################################

    colorize_svg(demo=True)


    foooo
    from cpblDefaults import WP
    swlv=tsvToDict(WP+'HRmeanSWL.csv',vectors=True)
    swl=dict(zip(tonumeric(swlv['PR_HRUID']),tonumeric(swlv['ss'])))

    #--------------------------------------------------------------------
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap as Basemap
    #from matplotlib.colors import rgb2hex
    from matplotlib.patches import Polygon



    # Lambert Conformal map of lower 48 states.
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
    # population density by state from
    # http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density
    popdensity = {
    'New Jersey':  438.00,
    'Rhode Island':   387.35,
    'Massachusetts':   312.68,
    'Connecticut':	  271.40,
    'Maryland':   209.23,
    'New York':    155.18,
    'Delaware':    154.87,
    'Florida':     114.43,
    'Ohio':	 107.05,
    'Pennsylvania':	 105.80,
    'Illinois':    86.27,
    'California':  83.85,
    'Hawaii':  72.83,
    'Virginia':    69.03,
    'Michigan':    67.55,
    'Indiana':    65.46,
    'North Carolina':  63.80,
    'Georgia':     54.59,
    'Tennessee':   53.29,
    'New Hampshire':   53.20,
    'South Carolina':  51.45,
    'Louisiana':   39.61,
    'Kentucky':   39.28,
    'Wisconsin':  38.13,
    'Washington':  34.20,
    'Alabama':     33.84,
    'Missouri':    31.36,
    'Texas':   30.75,
    'West Virginia':   29.00,
    'Vermont':     25.41,
    'Minnesota':  23.86,
    'Mississippi':	 23.42,
    'Iowa':	 20.22,
    'Arkansas':    19.82,
    'Oklahoma':    19.40,
    'Arizona':     17.43,
    'Colorado':    16.01,
    'Maine':  15.95,
    'Oregon':  13.76,
    'Kansas':  12.69,
    'Utah':	 10.50,
    'Nebraska':    8.60,
    'Nevada':  7.03,
    'Idaho':   6.04,
    'New Mexico':  5.79,
    'South Dakota':	 3.84,
    'North Dakota':	 3.59,
    'Montana':     2.39,
    'Wyoming':      1.96,
    'Alaska':     0.42}
    print shp_info
    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    cmap = plt.cm.hot # use 'hot' colormap
    vmin = 0; vmax = 450 # set range.
    print m.states_info[0].keys()
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico']:
            pop = popdensity[statename]
            # calling colormap with value between 0 and 1 returns
            # rgba value.  Invert color range (hot colors are high
            # population), take sqrt root to spread out colors more.
            colors[statename] = cmap(1.-np.sqrt((pop-vmin)/(vmax-vmin)))[:3]
        statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
            #color = rgb2hex(colors[statenames[nshape]]) 
            color = rgb_to_hex(colors[statenames[nshape]]) 
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    # draw meridians and parallels.
    m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
    plt.title('Filling State Polygons by Population Density')
    plt.show()



    # SOMETHING ELSE STARTS BELOW HERE...
    
    from pylab import mean
    if 1 and 'csrv' in  os.uname()[1]:

        from mpl_toolkits.basemap import Basemap

        mcool=tonumeric([LL.strip().split('\t') for LL in open('mcool.tsv','rt').readlines()])
        colour=assignColormapEvenly(mcool[::16],[swl.get(agg['PRHRuid'],nan) for agg in gg])
        plt.figure(3)
        plt.clf()
        proj='ortho'
        proj='cyl'
        map=Basemap(projection=proj,lat_0=50,lon_0=-100, area_thresh=1000.)
        #map.bluemarble() This is no good sicne coordinates are not in geographic!
        allpatches=[]
        for agg in sorted(gg,key=lambda x:swl.get(x['PRHRuid'],nan),reverse=True): # Order them for legend.
            map.plot(agg['Lon'],agg['Lat'],'y',linewidth=0)
            patches=plt.fill(agg['Lon'],agg['Lat'],edgecolor=None,facecolor=colour[swl.get(agg['PRHRuid'],nan)],label='%.2f: %s'%(swl.get(agg['PRHRuid'],nan),agg['HRname']))#str((agg['PRHRuid']-5900)/100.0))
            allpatches+=[patches]
        plt.axis('image')
        plt.ylim([1700000,3550000])
        plt.xlim([3670000.0, 4723366.4643540001])


        #map.drawmapboundary('w',linewidth=0)# ie turn it off

        plt.savefig('/home/cpbl/rdc/workingData/BCSWB.svg')
        plt.savefig('/home/cpbl/rdc/workingData/BCSWB.png',dpi=300)
        woeiru
        #plt.savefig('/home/cpbl/rdc/workingData/BCSWB.pdf')
        legend()
        plt.setp(allpatches,'visible',False)
        xx=mean(xlim())
        yy=mean(ylim())
        text(xx,yy,'Mean life satisfaction\n(1 to 5 scale)')

        text(xx,yy,"""C P Barrington-Leigh
    University of British Columbia
    Source: CCHS 2003-2006""")

        plt.savefig('/home/cpbl/rdc/workingData/BCSWB_legend.svg')

        #plt.savefig('/home/cpbl/rdc/workingData/BCSWB.svg')

    elif 1:
        legendText='\n'.join([''])
        # sorted(swl.items(),key=lambda x:x[1])])
        # for agg in sort(gg,key=lambda x:x['ss'])])
        xx=mean(xlim())
        yy=mean(ylim())
        plt.text(1800000,4000000,'woeiurw\noiudflkjn\nalksjdf')
        plt.plot([xx],[yy],'kx')
        plt.text(xx,yy,'woeiurw\noiudflkjn\nalksjdf')

    else:
        plt.figure(2)
        plt.clf()
        for agg in gg:
            plt.fill(agg['Lon'],agg['Lat'],facecolor=(1,1,(agg['PRHRuid']-5900)/100.0))

        foi
        plt.colormap('jet')
    #map.pcolor(agg['Lon'],agg['Lat'],swl.get(agg['PRHRuid'],0)*1.0/4.0)




    fooo













    if os.uname()[1] in['csrv']:

        from mpl_toolkits.basemap import Basemap
        import matplotlib.pyplot as plt

        # set up orthographic map projection with
        # perspective of satellite looking down at 50N, 100W.
        # use low resolution coastlines.
        # don't plot features that are smaller than 1000 square km.
        proj='ortho'
        proj=None
        if 0:
            map = Basemap(projection=proj,lat_0=50,lon_0=-100, resolution='l',area_thresh=1000.)
        else:
            map=Basemap(projection=proj,lat_0=50,lon_0=-100, area_thresh=1000.)
        # draw coastlines, country boundaries, fill continents.
        map.drawcoastlines()
        map.drawcountries()
        map.bluemarble()
        if 0:
            map.fillcontinents(color='coral')
        # draw the edge of the map projection region (the projection limb)
        map.drawmapboundary()
        # draw lat/lon grid lines every 30 degrees.
        map.drawmeridians(np.arange(0,360,30))
        map.drawparallels(np.arange(-90,90,30))
        plt.show()





    if os.uname()[1] in['cpbl-server']:

        import matplotlib.pyplot as plt
        #from mpl_toolkits.basemap import Basemap as Basemap
        import osgeo.ogr
        import cpblDefaults
        reload(cpblDefaults)
        defaults=cpblDefaults.defaults()


        #cc=osgeo.ogr.Open('/home/cpbl/tmp/countries_c.dat')
        cc=osgeo.ogr.Open(defaults['inputPath']+'healthRegions/shp/HR000b07_PZ.shp')


        layer=cc.GetLayer()
        numFeatures = layer.GetFeatureCount()
        print 'Feature count: ' + str(numFeatures)
        print 'Feature count:', numFeatures
        # Get the extent as a tuple (sort of a non- modifiable list)
        extent = layer.GetExtent()
        print 'Extent:', extent
        print 'UL:', extent[0], extent[3]
        print 'LR:', extent[1], extent[2]


        feature = layer.GetFeature(10)
        geometry = feature.GetGeometryRef()
        x = geometry.GetX()
        y = geometry.GetY()

        foi
        # Or we can loop through all of the features
        feature = layer.GetNextFeature()
        while feature:
          # do something here
          feature = layer.GetNextFeature()
        layer.ResetReading() #need if looping again


