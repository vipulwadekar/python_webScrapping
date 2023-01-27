import csv
fieldnames = ['player_name', 'fide_rating']
try :
    with open('players.csv', 'r', newline='') as file:
        with open('players.csv', 'a', newline='') as file:
          
            writer = csv.DictWriter(file,fieldnames=fieldnames)

    
            writer.writerow({'player_name': 'vikram Carlsen', 'fide_rating': 2870})
            writer.writerow({'player_name': 'ashish wadekar', 'fide_rating': 21801})
except FileNotFoundError as error:
    print(error,"rrrrr")
    with open('players.csv', 'a', newline='') as file:
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerow({'player_name': 'diguy', 'fide_rating': 2822})
        writer.writerow({'player_name': 'vipul wadekar', 'fide_rating': 2801})
except Exception as error:
    print(error)      