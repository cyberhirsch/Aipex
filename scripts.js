// Your Firebase configuration (replace with your Firebase project config)
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT_ID.firebaseio.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// Add Model Form Handling
document.getElementById('addModelForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const modelName = document.getElementById('modelName').value;
  const modelCategory = document.getElementById('modelCategory').value;

  db.ref('models/').push({
    name: modelName,
    category: modelCategory,
    votes: 0
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
      modelRef.update({ votes: currentVotes + 1 });
    }
  });
}
