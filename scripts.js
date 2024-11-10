// Aipex Project - Firebase Configuration
// Note: Configuration is already initialized in HTML, so we don't need to redeclare it here

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
