var kanban

async function fetchColonnes() {
    // Récupération des colonnes/tache via l'API
    const response = await fetch('http://127.0.0.1:8000/api/colonne/');
    const colonnes = await response.json();

    // Conversion des données pour le format attendu par jKanban
    const kanbanData = colonnes.map(colonne => ({
        id: colonne.id_colonne.toString(),
        title: colonne.titre_colonne,
        item: colonne.tache.map((tache, index) => ({
        id: tache.id_tache.toString(),
        title: tache.titre_tache,
        position: tache.position_tache,
        }))
    }));

        // Création d'un nouvel objet jKanban avec les données récupérées
        kanban = new jKanban({
            element: '#kanban',
            gutter: '15px',
            widthBoard: '250px',
            responsivePercentage: true,
            dragBoards: true,
            dragItems: true,
            boards: kanbanData,
            addItemButton: true,
            buttonContent: '+',
            click: function(el){


            
            },
            dropEl: function(el, target, source, sibling){
                //console.log('id colonne final ' + target.parentElement.getAttribute('data-id'));
                //console.log('id colonne depart ' + source.parentElement.getAttribute('data-id'));
                //console.log('id tache ' + el.getAttribute('data-eid'));

                console.log(el.previousSibling);
                console.log(el.nextSibling);
                
                colonne =  parseInt(target.parentElement.getAttribute('data-id'))
                idTache = parseInt(el.getAttribute('data-eid'))

                if(el.previousSibling != null){

                    position = parseInt(el.previousSibling.getAttribute('data-position')) + 1;

                }else if(el.nextSibling != null){

                    position = el.nextSibling.getAttribute('data-position');

                }else{

                    position = 1
                    
                }

                console.log('tache ' + idTache + " colonne " + colonne + " position " + position);

                switchTache(idTache, colonne, position)

            },
            dragendBoard: function(el){

                // id de la colonne déplacé
                idColonne = parseInt(el.getAttribute('data-id'));

                //new position de la colonne
                position = el.getAttribute('data-order')
               
                //console.log("colonne " + idColonne + " position " + position);
                switchColone(idColonne ,position)

            }        
        },

    );
    
    const listColonnes = document.querySelectorAll(".kanban-title-board");
    listColonnes.forEach(element =>{

        element.classList.add('card');  
        titre = element.innerHTML
        console.log(titre);
        element.removeChild(element.firstChild);

        let html = '';
        html += '<div class="card-body">';
        html += '<h5 class="card-title">' + titre + '</h5>';
        html += '<div class="d-flex">';
        html += '<a href="#" class="btn btn-outline-primary" id="'+ element.parentElement.parentElement.getAttribute('data-id')+'" onClick="addTache(this)">Add Task</a>';
        html += '<a href="#" class="btn btn-outline-danger" id="'+ element.parentElement.parentElement.getAttribute('data-id')+'" onClick="deleteColonne(this.id)">Delete</a>';
        html += '</div>';
        html += '</div>';

        element.innerHTML += html

    });   

    const listTache = document.querySelectorAll(".kanban-item");
    listTache.forEach(element => {

        element.classList.add('card');  
        titre = element.innerHTML;
        element.removeChild(element.firstChild);

        let html = '';
        html += '<div class="card-body">';
        html += '<h5 class="card-title">' + titre + '</h5>';
        html += '<p class="card-text"></p>';
        html += '<div class="d-flex">';
        html += '<a href="#" class="btn btn-outline-primary" id="'+ element.getAttribute('data-eid')+'" onClick="prepUpdate(this.parentElement)">Update</a>';
        html += '<a href="#" class="btn btn-outline-danger" id="'+ element.getAttribute('data-eid')+'" onClick="deleteTask(this)">Delete</a>';
        html += '</div>';
        html += '</div>';
       
        element.innerHTML += html

    });   

}

/**
 * Update la position de la colonne
 *
 * @param {number} colonne colonne ou ce situe la tache
 * @param {number} positionTache position de la tache dans la colonne
 * 
 */
async function switchTache(idTache, colone, position){
    var data = {
        'id_colonne' : colone,
        'position_tache' : position
    }
    console.log(data);

    var response = await fetch('http://localhost:8000/api/tache/'+ idTache +'/',{
                method:'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
    });
    var responseData = await response.json();
    
}

/**
 * Update la position de la colonne
 *
 * @param {number} positionColonne nouvelle position de la colonne
 * 
 */
async function switchColone(idColonne ,position){
    data = {
        'position_colonne' : position,
        
    }
    var response = await fetch('http://localhost:8000/api/colonne/'+ idColonne +'/',{
                    method:'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        
                    },
                    body: JSON.stringify(data)
    });
    var responseData = await response.json();
}


/**
 * Ajoute un tache 
 * 
 * @param {dom} element id la colonne ou l'on ajoute la tache
 * 
 */
async function addTache(element){
    titreTache = prompt('titre de la tache');
    id = element.getAttribute('id')

    data = {
        'titre_tache' : titreTache,
        'position_tache' : 0,
        'id_colonne' : id
    }

    console.log(data);

    var response = await fetch('http://localhost:8000/api/tache/',{
        method:'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
    })

    const responseJson = await response.json();
    console.log(responseJson);

    newTache = {
        id : responseJson.id_tache,
        title : responseJson.titre_tache,
        position : responseJson.position_tache
    }

    //kanban.addElement(id, newTache);

}

/**
 * Fonction qui supprime la tache
 * 
 * @param {dom} element id de la tache a supprimer
 * 
 */
async function deleteTask(element){
    console.log(element);
    idTache = element.getAttribute('id')
    idColonne = element.parentElement.parentElement.parentElement.getAttribute('data-eid')

    await fetch('http://localhost:8000/api/tache/'+ idTache,{
                method:'delete',
                headers: {
                    'Content-Type': 'application/json'
                },
                
    });

    kanban.removeElement(idColonne, idTache);
}

/**
 * Prepare les donnes pour la modification
 * 
 * @param {dom} element id de la tache a supprimer
 * 
 */
function prepUpdate(element){

    console.log(element);
        
    titreTache = prompt('nouveau titre')
    if(titreTache != null){

        idTache = parseInt(element.getAttribute('data-eid'))
        colonne =  parseInt(element.parentElement.parentElement.getAttribute('data-id'))
        position = parseInt(element.getAttribute('data-position'))
        updateTask(idTache,titreTache,colonne,position)
    }

}

/**
 * Update titre de la tache
 * 
 * @param {dom} idTache id de la tache a modifier
 * @param {string} titreTache titre de la tache
 * @param {number} colonne colonne ou ce situe la tache
 * @param {number} position position de la tache
 * 
 */
async function updateTask(idTache,titreTache,colonne,position){
    data = {
        'id_tache' : idTache,
        'titre_tache' : titreTache,
        'position_tache' : position,
        'id_colonne' : colonne
    }

    var response = await fetch('http://localhost:8000/api/tache/'+ idTache + '/',{
        method:'put',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
    })

}

/**
 * Ajouter Colonne
 * 
 * 
 * 
 */
async function addColonne(){

    titreColonne = prompt('titre de la colonne');

    data = {
        'titre_colonne' : titreColonne,
        'position_colonne' : 0

    }

    var response = await fetch('http://localhost:8000/api/colonne/',{
        method:'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
    })

    const responseJson = await response.json();
    console.log(responseJson);


    kanban.addBoards([
        {
            id: responseJson.id_colonne,
            title: responseJson.titre_colonne,
            
        }
    ]);

    element = document.querySelector('.kanban-board[data-id="'+ responseJson.id_colonne +'"]');

    console.log(element);

    element.removeChild(element.firstChild);
    element.classList.add('card');

    let html = '';
    html += '<div class="card-body">';
    html += '<h5 class="card-title">' + responseJson.titre_colonne + '</h5>';
    html += '<p class="card-text"></p>';
    html += '<div class="d-flex">';
    html += '<a href="#" class="btn btn-outline-primary" id="'+ responseJson.id_colonne +'" onClick="prepUpdate(this.parentElement)">Update</a>';
    html += '<a href="#" class="btn btn-outline-danger" id="'+ responseJson.id_colonne +'" onClick="deleteTask(this)">Delete</a>';
    html += '</div>';
    html += '</div>';
   
    element.innerHTML += html
}

/**
 * Supprimer Colonne
 * @param {number} idColonne id de la colonne a suprimer
 * 
 */
async function deleteColonne(idColonne){

        await fetch('http://localhost:8000/api/colonne/'+ idColonne,{
            method:'delete',
            headers: {
                'Content-Type': 'application/json'
        },

    });

    kanban.removeBoard(idColonne)

}


// Appel de la fonction pour afficher le kanban
fetchColonnes();
