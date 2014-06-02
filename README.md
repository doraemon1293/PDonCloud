PDonCloud
=========

URL:
doraemon1293513.appspot.com

plagiarism detection based on 3 different cloud computing platforms -- GoogleAppEngine(GAE), AmazonWebService EC2 and OpenStack.

The user's interface is on GAE. 
EC2 analyses source files to generate the indices. The generating is dynamic so the source files can be added, deleted or edited at any time.
OpenStack gets requests from GAE, analyses suspicious files, gets the indices from EC2, compares them and sends the results to GAE.

This system compares suspicious files and source files according to the user specified window size and overlap size to find out the plagiarism
For example:
If window size is 8 and overlap size is 2:
yesterday upon the stair i met a man who was not there he was not there again today i wish that man would go away will be transformed to:

yesterday upon the stair i met a man
 a man who was not there he was
 he was not there again today i wish
 i wish that man would go away


demo.gif shows how the system works.
report.pdf contains the detailed architecture

In source folder doraemon1293513 is for GAE.
match_main.py is for the main node in OpenStack.
matching,py is for the children nodes in OpenStack.
build_index.py is for using in EC2 to build the source index.

