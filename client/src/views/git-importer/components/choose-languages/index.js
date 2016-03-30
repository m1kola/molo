import React from 'react';
import includes from 'lodash/includes';


const ChooseLanguages = (d) => (
  <div className="c-choose-languages">
    <ul className="o-input-group">
    {d.languages.map(language =>
    <li
      key={language.name}
      className="o-input-group__item c-choose-languages__language">
      {/* TODO make it clear that main language is always checked */}
      <input
        type="checkbox"
        disabled={language.isMain}
        defaultChecked={language.isMain}
        onChange={() => d.actions.toggleLanguageChosen(language.id)} />
      <span className="o-input-group__label">{language.name}</span>
    </li>
    )}
    </ul>

    <div className="o-button-group">
      <button
        type="button"
        className={checkButtonClasses(d.status)}
        disabled={checkButtonDisabled(d.status)}
        onClick={() => d.actions.checkContent(d.site.id, d.languages)}>
        {checkButtonText(d.status)}
      </button>

      <button
        type="button"
        className={importButtonClasses(d.status)}
        disabled={importButtonDisabled(d.status)}
        onClick={() => d.actions.importContent(d.site.id, d.languages)}>
        {importButtonText(d.status)}
      </button>
    </div>
  </div>
);


function checkButtonText(status) {
  switch (status) {
    case 'CHECK_CONTENT_BUSY':
      return `Checking for errors...`;

    case 'CHECK_CONTENT_COMPLETE':
      return `No errors found`;

    case 'CHECK_CONTENT_ERROR':
      return `Errors found`;

    default:
      return `Check for errors`;
  }
}


function importButtonText(status) {
  switch (status) {
    case 'IMPORT_CONTENT_BUSY':
      return `Importing content...`;

    case 'IMPORT_CONTENT_COMPLETE':
      return `Import complete`;

    case 'IMPORT_CONTENT_ERROR':
      return `Could not import content`;

    default:
      return `Import`;
  }
}


function checkButtonClasses(status) {
  switch (status) {
    case 'CHECK_CONTENT_BUSY':
      return 'o-button c-choose-languages__check';

    case 'CHECK_CONTENT_COMPLETE':
      return 'o-button o-button--success c-choose-languages__check';

    case 'CHECK_CONTENT_ERROR':
      return 'o-button o-button--failure c-choose-languages__check';

    default:
      return 'o-button c-choose-languages__check';
  }
}


function importButtonClasses(status) {
  switch (status) {
    case 'IMPORT_CONTENT_BUSY':
      return 'o-button c-choose-languages__import';

    case 'IMPORT_CONTENT_COMPLETE':
      return 'o-button o-button--success c-choose-languages__import';

    case 'IMPORT_CONTENT_ERROR':
      return 'o-button o-button--failure c-choose-languages__import';

    default:
      return 'o-button c-choose-languages__import';
  }
}


function checkButtonDisabled(status) {
  return status !== 'IDLE';
}


function importButtonDisabled(status) {
  return !includes(['IDLE', 'CHECK_CONTENT_COMPLETE'], status);
}



export default ChooseLanguages;
