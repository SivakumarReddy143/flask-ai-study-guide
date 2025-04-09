from app import create_app

app = create_app()

if __name__ == "__main__":
    print("----------------------------------------")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("-----------------------------------")
    app.run(debug=True)