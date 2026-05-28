#--------------------------Data Retrievel Part and Publising Into Streamlit
# streamlit UI
#--------------------------
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

#------------------
# MYSQL Connection
#----------------------

db_host = "localhost"
db_user = "root"
db_pass = "root"
db_name = "global_seismic_proj1"

#-- Establishing connection Between MYSQL And Python

engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}")
print("✅ Env Setup Done, Connected to MYSQL Successfully")

st.title(" 🌍Earthquake Data Analysis Dashboard")
st.write(" 📌Select any problem statement (1-30) to run the corresponding SQL query & to see the result")

queries = {
        "Q1": """SELECT * FROM eq_data 
               ORDER BY mag DESC 
               LIMIT 10
               """,
        "Q2": """ SELECT * FROM eq_data
               ORDER BY depth_km DESC
               LIMIT 10 
               """,
        "Q3": """SELECT * FROM eq_data 
               WHERE depth_km <50 AND mag >7.5 
               """,
        "Q4": """SELECT country1, AVG(depth_km) as avg_depth
               FROM eq_data 
               GROUP BY country1 
               ORDER BY avg_depth DESC
               """,
        "Q5": """ SELECT magType, AVG(mag) as avg_mag FROM eq_data
               GROUP BY magType 
               ORDER BY avg_mag DESC
               """,
        "Q6": """ SELECT year, COUNT(year) as total FROM eq_data
               GROUP BY year
               ORDER BY  cout_year DESC 
               LIMIT 10""",
        "Q7": """ SELECT month, COUNT(month) as total FROM eq_data
               GROUP BY month
               ORDER BY  total DESC
               LIMIT 10 """,
        "Q8": """ SELECT day_of_week, COUNT(day_of_week) as total FROM eq_data
               GROUP BY day_of_week
               ORDER BY  total DESC
               LIMIT 10 """,
        "Q9": """ SELECT HOUR(time), COUNT(*) as total FROM eq_data
               GROUP BY HOUR(time)
               ORDER BY  total DESC
               LIMIT 10 """,
        "Q10": """ SELECT net, COUNT(*) as total FROM eq_data
               GROUP BY net
               ORDER BY  total DESC
               LIMIT 10 """,
        "Q11": """ SELECT place, MAX(felt) as casualities FROM eq_data
               GROUP BY place
               ORDER BY  casualities DESC
               LIMIT 10 """,
        "Q12": """ SELECT country1, AVG(MAG) as avg_mag FROM eq_data
               GROUP BY country1
               ORDER BY avg_mag DESC
               LIMIT 10
               """,
        "Q13": """ SELECT alert, AVG(depth_km) as avg_depthkm FROM eq_data
               GROUP BY alert
               ORDER BY  avg_depthkm DESC
               LIMIT 10 """,
        "Q14": """SELECT status, COUNT(*) as total FROM eq_data
               GROUP BY status """,
        "Q15": """ SELECT type, COUNT(*) as total FROM eq_data
               GROUP BY type
               LIMIT 10 """,
        "Q16": """ SELECT types, COUNT(*) as total FROM eq_data
               GROUP BY types
               LIMIT 10 """,
        "Q17": """ SELECT country1, AVG(rms) as avg_rms, AVG(gap) as avg_gap FROM eq_data
               GROUP BY country1
               LIMIT 10 """,
        "Q18": """ SELECT * FROM eq_data
               WHERE nst>40                              
               LIMIT 10 """,
        "Q19": """SELECT  YEAR(time) as year, COUNT(*) as total FROM eq_data
               WHERE tsunami = 1 
               GROUP BY YEAR(time)""",
        "Q20": """SELECT  alert, COUNT(*) as total FROM eq_data
               WHERE type = "earthquake" 
               GROUP BY alert 
               """,
        "Q21": """SELECT country1,  ROUND(AVG(mag), 2) AS avg_mag FROM eq_data
               WHERE year >= YEAR(CURDATE())-2
               GROUP BY country1
               ORDER BY avg_mag DESC
               LIMIT 5""" ,
        
        "Q22": """SELECT DISTINCT country1 , month FROM eq_data
               WHERE depth_flag IN ("shallow", "deep")
               GROUP BY country1,year,month
               HAVING COUNT(DISTINCT depth_flag) = 2
               ORDER BY country1
               LIMIT 10""",
        "Q23": """SELECT year, COUNT(*) as total FROM eq_data
               WHERE type = "earthquake"
               GROUP BY year
               ORDER BY year""",
        "Q24": """SELECT country1, 
               COUNT(*) as frquency ,
               ROUND(AVG(mag),2) as avg_mag, 
               ROUND(COUNT(*) * AVG(mag),2) as activity_score 
               FROM eq_data
               WHERE type = "earthquake"
               GROUP BY country1
               ORDER BY activity_score DESC
               LIMIT 3""",
        "Q25": """SELECT country1, ROUND(AVG(depth_km),2) as avg_depthkm FROM eq_data
               WHERE latitude BETWEEN -5 AND 5
               GROUP BY country1
               ORDER BY avg_depthkm DESC
               LIMIT 5""",
        "Q26": """SELECT country1,
           SUM(CASE WHEN depth_flag='shallow' THEN 1 ELSE 0 END) AS shallow_count,
           SUM(CASE WHEN depth_flag='deep' THEN 1 ELSE 0 END) AS deep_count
               FROM eq_data
               GROUP BY country1
               HAVING deep_count > 0""",
        "Q27": """SELECT tsunami,
              ROUND(AVG(mag), 2) AS avg_mag
              FROM eq_data
              GROUP BY tsunami""",
        "Q28": """SELECT id,place,gap,rms, ROUND((gap + rms), 2) AS error_score
               FROM eq_data
               WHERE gap IS NOT NULL
                AND rms IS NOT NULL
                ORDER BY error_score DESC
               LIMIT 10""",
         "Q29": """WITH eq_pairs AS (
               SELECT
               id,
               time,
               latitude,
               longitude,

        LEAD(id) OVER (ORDER BY time) AS next_id,
        LEAD(time) OVER (ORDER BY time) AS next_time,
        LEAD(latitude) OVER (ORDER BY time) AS next_lat,
        LEAD(longitude) OVER (ORDER BY time) AS next_lon

               FROM eq_data
)              SELECT
               id,
               next_id,
               time,
                next_time,

          TIMESTAMPDIFF(MINUTE, time, next_time) AS time_diff_minutes,

              ROUND(
              111 * SQRT(
              POW(next_lat - latitude, 2) +
              POW(next_lon - longitude, 2)
        ),
        2
    ) AS distance_km

FROM eq_pairs

WHERE TIMESTAMPDIFF(MINUTE, time, next_time) <= 60

AND (
    111 * SQRT(
        POW(next_lat - latitude, 2) +
        POW(next_lon - longitude, 2)
    )
) <= 50
""",
        "Q30": """SELECT country1,
               COUNT(*) AS deep_focus_frequency
               FROM eq_data
               WHERE depth_km > 300
               GROUP BY country1
               ORDER BY deep_focus_frequency DESC
               LIMIT 10
"""
               
}

task = st.selectbox("🔍Choose the task number here in the dropdown list please:", list(queries.keys ()))

if st.button(" ▶ Run the selected task"):
    query = queries[task]
    eq_df = pd. read_sql(query, engine)
    
    st.subheader(f"Results for: {task}")
    st.dataframe(eq_df, use_container_width=True)
