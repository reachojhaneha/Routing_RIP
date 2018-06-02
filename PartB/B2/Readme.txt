As it can be seen from the output, inititally it takes around 3 secs to converge. 
To determine convergence time I'm using the ping command. By implementation ping sends packets every 1 sec on unsuccessful ping. So as soon as the setup is done I'm sending some ping command from h1 to h2. This gives the number of seconds it takes for the algorithm to converge.

These 3.05957198143s includes intital setup and convergence time.
