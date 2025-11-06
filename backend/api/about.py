from fastapi import APIRouter

router = APIRouter(prefix="/about", tags=["about"])

@router.get("/")
async def get_about_info():
    """Return information about Shellmates club."""
    return {
        "name": "Shellmates",
        "description": "Shellmates is a scientific club dedicated to cybersecurity at the Higher National School of Computer Science (ESI), Algiers, Algeria. It is a group of highly motivated university students that are passionate about information security in general. Its diversity of members who are from different Wilayas & different universities is what makes it a special one. \n/* Where there is a Shell, There is a way */",
        "founded": "2011",
        "mission": "Encourage hands-on learning through workshops and challenges. \nTeach and inspire anyone passionate about cybersecurity. \nDevelop technical and soft skills essential for cybersecurity careers. \nBuild a strong cybersecurity community. \nReduce time and efforts to achieve goals.",
        "our community": "From the very first beginning, Shellmates club ultimate goal was to set the seal on creating an infoSec community by spreading the knowledge about information security, which kept our community growing day by day. Thanks to our members' hard work and dedication, we could reach a total of 12k followers on our social media and 2k on our discord community server.",
        "departments": [
            {
                "name": "Technical Department",
                "description": "The builders of the club! \nThis team works on creating and maintaining our digital platforms and tools. Developing the club’s website or applications. Automating tasks to improve efficiency. Focus on CTF competitions and problem-solving challenges."
            },
            {
                "name": "Development Department",
                "description": "The problem-solvers and innovators! \nThis department ensures all technical aspects of the club run smoothly. Work on the club’s tech-related projects (CTF..). Organize technical workshops for members."
            },
            {
                "name": "Design Department",
                "description": "The source of creativity and the visual identity of the club! \nDesigning social media posts and event banners. Exploring UX/UI for web or mobile projects."
            },
            {
                "name": "Sponsoring & Relax Department",
                "description": "The bridge to the outside world! \nThis team focuses on building relationships with sponsors and partners to support our projects. Contacting potential sponsors and negotiating deals. Managing partnerships for events or long-term collaboration."
            },
            {
                "name": "Multimedia Department",
                "description": "The storytellers through visuals! \nThis team captures moments and turns them into memories. Taking photos and videos at events, Creating highlight reels and after-movies, Editing visual content to share on social platforms."
            },
            {
                "name": "Communication Department",
                "description": "The voice of the club! \nThis team spreads our message to the world and keeps members updated. Manage the club’s image and voice on social media. Maintaining a positive image of the club online."
            },
            {
                "name": "Events Department",
                "description": "The fun soul of the club! \nBrings fresh ideas, animates sessions, and organizes both internal and external activities. Plans engaging events, workshops, and gatherings that keep members motivated and connected."
            },
            {
                "name": "Human Resources Department",
                "description": "trackers of the club! \nCreates a welcoming environment, strengthens internal bonds, and makes sure every member feels part of the family."
            }
        ],
        "activities": [
            "ShellMates CTF - Annual Capture The Flag competition",
            "Weekly workshops and training sessions",
            "Hack.ini - Training program for beginners",
            "Participation in international cybersecurity competitions",
            "Technical talks and conferences"
        ],
        "contact": {
            "website": "https://www.shellmates.club/",
            "email": "shellmates@esi.dz",
            "location": "École nationale supérieure d'informatique BPM68 16270, Oued Smar, Algiers, Algeria"
        }
    }