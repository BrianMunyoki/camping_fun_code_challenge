

app=Flask(__name__)

@app.route('/')

def home():
    return "API is running!"

if __name__=="__main__":
    app.run(port=5555,debug=True)