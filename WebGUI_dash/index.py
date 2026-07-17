from app import app
from layout import layout
import callbacks

app.layout = layout

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8050)