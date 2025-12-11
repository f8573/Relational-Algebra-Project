Here's how to use this.
radb is the frontend, radb-core is the backend.
To use, run these commands in order.

cd backend
pip install
pip install -e .
python server.py

Open frontend/index.html in browser to your heart's content. However, as I've removed the .db file, you'll be working with a completely blank one.
You'll need to navigate to the Raw LaTeX tab, and write out some SQL commands.

e.g. :

\sqlexec_{CREATE TABLE R(a int, b int)};
\sqlexec_{INSERT INTO R VALUES (1, 2)};

And then navigate back to whatever you choose to write your queries in. An example following our basic example schema is:

\sigma_{a=1}(R)

Please open an issue if anything goes wrong.