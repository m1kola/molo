export function expandStep(name) {
  return {
    type: 'expand-step',
    name: name
  };
}


export function chooseSite() {
  return {type: 'choose-site'};
}


export function chooseMain() {
  return {type: 'choose-main'};
}


export function changeSite(id) {
  return {
    type: 'change-site',
    id: id
  };
}


export function changeMain(id) {
  return {
    type: 'change-main',
    id: id
  };
}


export function toggleLanguageChosen(id) {
  return {
    type: 'toggle-language-chosen',
    id: id
  };
}


export function importContent() {
  return {type: 'import-content'};
}