import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDocog2_MQHjFY2kXmiyJRCfqR-Ov9DMQo",
  authDomain: "web-chat-696bc.firebaseapp.com",
  projectId: "web-chat-696bc",
  storageBucket: "web-chat-696bc.appspot.com",
  messagingSenderId: "894332175217",
  appId: "1:894332175217:web:efcfd34912772efefc6cd0"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);
export const db = getFirestore(app);
