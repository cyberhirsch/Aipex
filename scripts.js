// Your Firebase configuration (replace with your Firebase project config)
const firebaseConfig = {
  apiKey: "AIzaSyCrSS4lsxgSFA7SEtseW1KoiruQbUwR_xA",
  authDomain: "aipex-6d63b.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT_ID.firebaseio.com",
  projectId: "aipex-6d63b",
  storageBucket: "aipex-6d63b.firebasestorage.app",
  messagingSenderId: "356818143159",
  appId: "1:356818143159:web:49222b5a85629c4630ca32"
  measurementId: "G-D32Z47WHQ4"
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
