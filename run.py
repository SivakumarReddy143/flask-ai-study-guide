from app import create_app

app = create_app()

if __name__ == "__main__":
    print("----------------------------------------")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("-----------------------------------")
    # 🚀 This makes it accessible from outside the container
    app.run(host="0.0.0.0", port=5000, debug=True)
