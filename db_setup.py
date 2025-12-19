import sqlite3
import os

DB_NAME = 'health.db'

def get_specialty_name(specialty_id):
    mapping = {
        1: "General Physician (GP)",
        2: "Otolaryngologist (ENT)",
        3: "Gastroenterologist",
        4: "Dermatologist", 
        5: "Orthopedic"
    }
    return mapping.get(specialty_id, "General Physician (GP)")


def setup_database():

    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"🧹 Existing database {DB_NAME} deleted for fresh setup.")
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    

   

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Symptoms (
            symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_name TEXT NOT NULL UNIQUE,
            description TEXT,
            doctor_advice TEXT,
            priority INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Recommendations (
            rec_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rec_name TEXT NOT NULL,
            rec_type TEXT NOT NULL CHECK(rec_type IN ('Home Remedy', 'Dietary', 'Ayurvedic', 'Tablet')),
            instructions TEXT NOT NULL,
            disclaimer TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Symptom_Recommendation_Mapping (
            mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_id INTEGER NOT NULL,
            rec_id INTEGER NOT NULL,
            FOREIGN KEY (symptom_id) REFERENCES Symptoms (symptom_id) ON DELETE CASCADE,
            FOREIGN KEY (rec_id) REFERENCES Recommendations (rec_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Specialties (
            specialty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            specialty_name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Specialties (
            specialty_id INTEGER PRIMARY KEY AUTOINCREMENT,
            specialty_name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialty_id INTEGER NOT NULL,
            rating REAL,
            experience INTEGER,
            location_lat REAL,
            location_lon REAL,
            availability TEXT,
            email TEXT UNIQUE,
            password TEXT,
            specialty TEXT,           -- ADDED: Required for Flask Profile view
            biography TEXT,           -- ADDED: Required for Flask Profile view
            FOREIGN KEY (specialty_id) REFERENCES Specialties (specialty_id) ON DELETE CASCADE
        )
    ''')

    
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Symptom_Specialty_Mapping (
            map_id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptom_id INTEGER NOT NULL,
            specialty_id INTEGER NOT NULL,
            FOREIGN KEY (symptom_id) REFERENCES Symptoms (symptom_id) ON DELETE CASCADE,
            FOREIGN KEY (specialty_id) REFERENCES Specialties (specialty_id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_id INTEGER,
            appointment_date TEXT,
            appointment_time TEXT,
            status TEXT DEFAULT 'Pending',
            reason TEXT,       
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
        )
    ''')
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Health_History(
            user_id INTEGER,
            symptom_name TEXT,
            remedy_suggested TEXT,
            date_recorded TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS UserRecords (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    description TEXT,
    upload_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
    ''')

    
    symptoms = [
        ('headache', 'Pain or discomfort in the head or face.', 
         'Seek immediate help if headache is sudden and severe, accompanied by a stiff neck, confusion, or loss of consciousness.', 2),
        ('cough', 'A reflex action to clear your airways of mucus and irritants.', 
         'See a doctor if cough persists for more than 7 days, or is accompanied by blood or difficulty breathing.', 1),
        ('acidity', 'A burning sensation in the chest, also known as heartburn.', 
         'Consult a doctor if symptoms occur more than twice a week, or if pain spreads to your arm or jaw.', 1),
        ('fever', 'An increase in body temperature above the normal range (98.6°F / 37°C).', 
         'Seek medical attention if fever exceeds 103°F (39.4°C), or lasts longer than 3 days, or is accompanied by severe symptoms.', 3),
        ('joint pain', 'Discomfort, aches, and soreness in any of the body\'s joints.', 
         'Consult a doctor if the joint pain is severe, accompanied by sudden swelling, redness, or if movement is severely limited.', 2)
    ]

    recommendations = [
        ('Ginger Tea', 'Home Remedy', 'Boil fresh ginger slices in water for 10 minutes. Strain and drink warm.', 'Avoid if you have a bleeding disorder.'),
        ('Stay Hydrated', 'Dietary', 'Drink at least 8-10 glasses of water throughout the day.', None),
        ('Paracetamol', 'Tablet', 'Take one 500mg tablet. Do not exceed 4 tablets in 24 hours.', 'Consult a doctor if symptoms persist.'),
        ('Honey and Lemon', 'Home Remedy', 'Mix one tablespoon of honey and a few drops of lemon juice in warm water and sip slowly.', 'Do not give honey to children under 1 year old.'),
        ('Avipattikar Churna', 'Ayurvedic', 'Take 1-2 teaspoons with lukewarm water before meals.', 'Consult an Ayurvedic practitioner before use.'),
        ('Cold Milk', 'Dietary', 'Drink a glass of cold, plain milk to get instant relief from burning sensation.', 'Avoid if you are lactose intolerant.'),
        ('Tepid Sponge Bath', 'Home Remedy', 'Wipe the body with lukewarm water for cooling.', 'Avoid ice-cold water, as it can cause shivering.'),
        ('Rest and Ice', 'Home Remedy', 'Rest the affected joint and apply a cold pack for 15-20 minutes, 3 times a day.', 'Do not apply ice directly to the skin.'),
        ('Naproxen', 'Tablet', 'Take one 250mg tablet every 8 hours.', 'Consult a doctor if you have stomach problems or heart disease.'),
        ('Turmeric Milk', 'Dietary', 'Mix 1 teaspoon of turmeric powder in warm milk and drink before bed.', 'N/A')
    ]


    specialties_data = [
        ('General Physician (GP)', 'A doctor who provides routine care and manages common illnesses.'), # ID 1
        ('Otolaryngologist (ENT)', 'Specializes in the ear, nose, and throat.'), # ID 2
        ('Gastroenterologist', 'Specializes in the digestive system and its disorders.'), # ID 3
        ('Dermatologist', 'Specializes in conditions of the skin, hair, and nails.'), # ID 4 
        ('Orthopedic', 'Specializes in bones and joints.') # ID 5
    ]
    
    #  doctors_data format: (Name, specialty_id, rating, experience, lat, lon, availability, email, password)
    doctors_raw_data = [
        ('Dr. Priya Sharma', 1, 4.8, 12, 18.5204, 73.8567, 'Online/10:00-14:00', 'priya@gmail.com', '1234'),
        ('Dr. Anish Menon', 2, 4.5, 8, 18.5195, 73.8553, 'Offline/16:00-20:00', 'anish@gmail.com', 'abcd'),
        ('Dr. Sneha Varma', 3, 4.9, 18, 18.5220, 73.8580, 'Online/11:00-13:00', 'sneha@gmail.com', '5678'),
        ('Dr. Rohit Singh', 1, 4.2, 5, 18.5208, 73.8560, 'Offline/17:00-21:00', 'rohit@gmail.com', '9999'),
        ('Dr. Kabir Jain', 2, 4.7, 10, 18.5210, 73.8570, 'Online/15:00-17:00', 'kabir@gmail.com', '4321'),
        ('Dr. Sania Reddy', 5, 4.6, 9, 18.5225, 73.8585, 'Offline/09:00-14:00', 'sania@gmail.com', '2468')
    ]

    
    doctors_final_data = []
    for data in doctors_raw_data:
        specialty_text = get_specialty_name(data[1])
        # Create a detailed biography text using the data
        biography = f"{data[0]} is a board-certified {specialty_text} with {data[3]} years of experience. Available {data[6].split('/')[0]}."
        
        # New Tuple: (name, specialty_id, rating, experience, lat, lon, availability, email, password, specialty_TEXT, biography_TEXT)
        doctors_final_data.append(data + (specialty_text, biography))
        
    symptom_recommendation_mappings = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 4),
        (3, 5), (3, 6),
        (4, 3), (4, 7), (4, 10),
        (5, 8), (5, 9), (5, 10)
    ]

    symptom_specialty_mappings = [
        (1, 1), (2, 2), (2, 1),
        (3, 3), (4, 1),
        (5, 1), (5, 5)
    ]

   


    cursor.executemany("INSERT INTO Symptoms (symptom_name, description, doctor_advice, priority) VALUES (?, ?, ?, ?)", symptoms)
    cursor.executemany("INSERT INTO Recommendations (rec_name, rec_type, instructions, disclaimer) VALUES (?, ?, ?, ?)", recommendations)
    cursor.executemany("INSERT INTO Specialties (specialty_name, description) VALUES (?, ?)", specialties_data)
    

    cursor.executemany(
        """INSERT INTO Doctors 
        (name, specialty_id, rating, experience, location_lat, location_lon, availability, email, password, specialty, biography) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        doctors_final_data
    )
    
    cursor.executemany("INSERT INTO Symptom_Recommendation_Mapping (symptom_id, rec_id) VALUES (?, ?)", symptom_recommendation_mappings)
    cursor.executemany("INSERT INTO Symptom_Specialty_Mapping (symptom_id, specialty_id) VALUES (?, ?)", symptom_specialty_mappings)
    
    
    cursor.execute("INSERT INTO Users (user_id, name, email, password) VALUES (1, 'Test Patient 1', 'test@user.com', 'pass');")
    cursor.execute("INSERT INTO Appointments (user_id, doctor_id, appointment_date, appointment_time, status) VALUES (1, 1, '2025-11-15', '11:00', 'Pending');")


    conn.commit()
    conn.close()

    print(f"\n {DB_NAME} has been created and populated successfully with all data.")


if __name__ == "__main__":
    setup_database()