// Your Firebase configuration (make sure all properties are correct)
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT_ID.firebaseio.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID" // Optional, remove if not needed
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get a reference to the database
const db = firebase.database();

// Add Model Form Handling
document.getElementById('addModelForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const modelName = document.getElementById('modelName').value;
  const modelCategory = document.getElementById('modelCategory').value;

  // Push the new model to the database
  db.ref('models/').push({
    name: modelName,
    category: modelCategory,
    votes: 0
  }).then(() => {
    console.log("Model added successfully");
  }).catch((error) => {
    console.error("Error adding model:", error);
  });

  document.getElementById('addModelForm').reset();
});

// Retrieve and Display Models
db.ref('models/').on('value', function(snapshot) {
  const modelsList = document.getElementById('modelsList');
  modelsList.innerHTML = '';
  snapshot.forEach(function(childSnapshot) {
    const model = childSnapshot.val();
    const modelId = childSnapshot.key;
    const modelElement = document.createElement('div');
    modelElement.innerHTML = `
      <p><strong>${model.name}</strong> (${model.category}) - Votes: ${model.votes}</p>
      <button onclick="vote('${modelId}')">Vote</button>
    `;
    modelsList.appendChild(modelElement);
  });
});

// Voting Function
function vote(modelId) {
  const modelRef = db.ref('models/' + modelId);
  modelRef.get().then(function(snapshot) {
    if (snapshot.exists()) {
      const currentVotes = snapshot.val().votes;
      modelRef.update({ votes: currentVotes + 1 }).then(() => {
        console.log("Vote added successfully");
      }).catch((error) => {
        console.error("Error updating votes:", error);
      });
    }
  }).catch((error) => {
    console.error("Error fetching model:", error);
  });
}
