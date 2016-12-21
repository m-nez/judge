usage: gui.py [-h] [-g | -f FILE] [-s SIZE] [-x WIDTH] [-y HEIGHT] [-e]  
              [-t TIMEOUT] [-p]  
              prog1 prog2  

Judge the game between two programs  

positional arguments:  
  prog1                 first program  
  prog2                 second program  
  
optional arguments:  
  -h, --help            show this help message and exit  
  -g, --gui             run with gui (not available with -f)  
  -f FILE, --file FILE  Play games on boards with sizes stated in the file  
  -s SIZE, --size SIZE  dimensions of the board  
  -x WIDTH, --width WIDTH  
                        width of the gui  
  -y HEIGHT, --height HEIGHT  
                        height of the gui  
  -e, --enumerate       enumerate placed blocks  
  -t TIMEOUT, --timeout TIMEOUT  
                        maximal move time  
  -p, --step            Request the next step by pressing <Space>  
  
e.g.  
	python gui.py "python prog1.py" "python prog1.py" -g -s 7  
