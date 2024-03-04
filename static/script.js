/* Get important page elements */
const userName = document.getElementById("userName");
const popupSave = document.getElementById("popupSave");
const dateTimeNow = document.getElementById("dateTimeNow");
const btnSave = document.getElementById("btnSave");
const form = document.getElementById("form");
const btnLogout = document.getElementById("logout");


/* Close popup box */
function closePopup() {
    popupSave.className = "popupBoxe hidden";
}


/* local storage utility class  */
class Ls {
    constructor(key) {
        this.key = key;

    }
    set(value) {
        localStorage.setItem(this.key, value.toString());
    }

    get() {
       return localStorage.getItem(this.key);
    }

    delete() {
        localStorage.removeItem(this.key);
    }
    
}
const user = new Ls("userName");

/* Add listener to /getuser form */
form.addEventListener("submit", () => user.set(userName.value.toLowerCase()));

/* Add listener to log out button */
btnLogout.addEventListener("click", () => {
    user.delete();
    popupSave.className = "popupBox visible";
});

/* If a user name exists close popup */
if (user.get()) {
    closePopup();
}


/* Display the date */
const formatDate = (date = new Date()) => { 
    const value = user.get();
    const hello = ["Good morning", "Good afternoon"];
    const weekday = ["Sunday","Monday",
    "Tuesday","Wednesday",
    "Thursday","Friday","Saturday"];
    const month = ["January","February",
    "March","April","May","June",
    "July","August","September","October",
    "November","December"];
    const day = weekday[date.getDay()];
    const dayNumber = date.getDate();
    const monthName = month[date.getMonth()];
    const year = date.getFullYear();
    const hours = date.getHours()
    const ampm = hours >= 12 ? "pm" : "am";
    const userName = value ? value[0].toUpperCase() + value.slice(1) : "";
    let helloTime = "";
    if (ampm === "am") {
       helloTime =  hello[0]; 
    }else {
        helloTime = hello[1];
    }
    return `${helloTime} ${userName} ${"it's"} ${day} ${dayNumber.toString()} ${monthName} ${year.toString()}`
}

 

/* Display the time */
setInterval(() => {
    const d = new Date();
    dateTimeNow.innerText = formatDate(d) + " " + d.toLocaleTimeString()
}, 1000);