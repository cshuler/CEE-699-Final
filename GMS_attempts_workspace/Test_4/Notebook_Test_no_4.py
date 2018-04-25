
# coding: utf-8

# In[9]:


import numpy as np
import flopy
import matplotlib.pyplot as plt
import flopy.utils.binaryfile as bf

get_ipython().run_line_magic('matplotlib', 'notebook')


# make the screen bigger!
from IPython.display import display, HTML
display(HTML(data=""" <style>
    div#notebook-container    { width: 95%; }
    div#menubar-container     { width: 85%; }
    div#maintoolbar-container { width: 99%; } </style> """))


# In[10]:


# Assign name and create modflow model object
txtname = 'test_no_4'
model_name = flopy.modflow.Modflow(txtname, exe_name='mf2005')


# # Load up MODFLOW files from GMS into flopy
# these files need to be in the working directory, or can be pointed to 

# In[11]:


dis = flopy.modflow.ModflowDis.load('TutCoast_simple4.dis', model_name)       # this command is neededed to load an existing .dis file   (essentially is grid geometry)
bas = flopy.modflow.ModflowBas.load('TutCoast_simple4.ba6',model_name)        #  load an existing .basic package                         (essentially is ibound and starting heads)
lpf = flopy.modflow.ModflowLpf.load('TutCoast_simple4.lpf', model_name)       #  load an existing .lpf file    
rch = flopy.modflow.ModflowRch.load('TutCoast_simple4.rch', model_name)
hobs = flopy.modflow.ModflowHob.load('TutCoast_simple4.hob', model_name)



# addd the well package
wel = flopy.modflow.ModflowWel.load('TutCoast_simple4.wel', model_name)

# not sure why these generate different results
   # Add PCG package to the MODFLOW model
#pcg = flopy.modflow.ModflowPcg.load('TutCoast_simple3.pcg', model_name)    # COMMENT ONE OF THESE OUT
# Add PCG package to the MODFLOW model
pcg = flopy.modflow.ModflowPcg(model_name)


# In[12]:


# Add OC package to the MODFLOW model
spd = {(0, 0): ['print head', 'print budget', 'save head', 'save budget']}
oc = flopy.modflow.ModflowOc(model_name, stress_period_data=spd, compact=True)


# In[13]:


# Write the MODFLOW model input files
model_name.write_input()


# In[14]:


# Run the MODFLOW model
success, buff = model_name.run_model()


# In[15]:


# Post process the results

hds = bf.HeadFile(txtname + '.hds')
head = hds.get_data(totim=1.0)
levels = np.linspace(0, 10, 11)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1, 1, 1, aspect='equal')

hds = bf.HeadFile(txtname+'.hds')
times = hds.get_times()
head = hds.get_data(totim=times[-1])
levels = np.linspace(0, 10, 11)

cbb = bf.CellBudgetFile(txtname+'.cbc')
kstpkper_list = cbb.get_kstpkper()
frf = cbb.get_data(text='FLOW RIGHT FACE', totim=times[-1])[0]
fff = cbb.get_data(text='FLOW FRONT FACE', totim=times[-1])[0]

modelmap = flopy.plot.ModelMap(model=model_name, layer=0)
qm = modelmap.plot_ibound()
lc = modelmap.plot_grid()
cs = modelmap.contour_array(head, levels=levels)
quiver = modelmap.plot_discharge(frf, fff, head=head)


# plot well location
wel.plot()
