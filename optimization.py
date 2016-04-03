#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Lessons from doing tricky multi-variate optimization
 (n.b., cpbl: Also see osm_history.py)
"""

class OptimizationExplorer:
    """
    Gain insight into your problem by optimizing some of the variables by hand.
    This shows 1-D slices through the objective function for the variables you choose, and lets you change values graphically.
    """
    def __init__(self, msef,x, ix, callback=None):
        """
        msef: this is the objective function to be maximized (mean squared error, a function of parameters vector x)
        x: a vector of starting values for the arguments/parameters
        ix: a list of indices (into x) of the variables you want to visualize and change by hand.
        callback: an optional function (taking the vector x) which could do some additional plotting, each time user clicks a new value of a parameter.
        """
        self.msef=msef
        self.xparams=x
        self.iParamsToVary=ix
        self.plotcallback=callback
        self.saxes=np.array([subplot(len(ix),1,ii+1) for ii in range(len(ix))])
        self.xranges=None
        self.fig=plt.gcf()
        self.plotSlices()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self)
        
    def plotSlices(self):
        """
        This plots 1-D slices through the objective function.
        It just has a simple heuristic for choosing the range and density of values to plot: it uses no derivatives, etc.
        """
        for iib,ax in enumerate(self.saxes):
            bi=self.xparams[self.iParamsToVary[iib]]
            # TO Do: add to the following a range spanning the last chosen xrange in the plot
            bx=sorted(np.concatenate([ bi+arange(-1,1,.01),   bi*logspace(-3,2, 100), bi*(1+logspace(-2,1)),   bi*(1-logspace(-2,1)), ]))
            b0=self.xparams
            mse=[self.msef(np.concatenate([ b0[:iib],[bxi],b0[iib+1:]]))  for bxi in bx]
            ax.cla()
            ax.plot(bx,mse, '.-')
            ax.plot(bi, self.msef(b0), 's')
            if self.xranges is not None:
                ax.set_xlim(self.xranges[iib])
        self.fig.canvas.draw()
        
    def __call__(self, event):
        """
        This is the event handler for clicks in the plot window
        """
        if event.button==2:
            event.canvas.mpl_disconnect(event.canvas.manager.key_press_handler_id)
            return
        if event.button==1: return
        #print 'click', event
        new_b=event.xdata
        iParam=  np.where(np.array(self.saxes)==event.inaxes)[0][0]
        print(' Setting parameter %d to %f...'%(iParam,new_b))
        print self.xparams
        self.xparams[self.iParamsToVary[iParam]]=new_b
        self.xranges=[ax.get_xlim() for ax in self.saxes]
        self.plotSlices()
        if self.plotcallback is not None:
            self.plotcallback(event.xparams)

