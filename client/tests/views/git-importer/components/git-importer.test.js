import { spy } from 'sinon';
import { expect } from 'chai';
import { shallow, mount } from 'enzyme';
import React from 'react';
import fixtures from 'tests/views/git-importer/fixtures';
import GitImporter from 'src/views/git-importer/components/git-importer';


describe(`GitImporter`, () => {
  it(`should render disabled and enabled steps`, () => {
    const state = fixtures('git-importer');
    state.steps.site.isDisabled = false;
    state.steps.main.isDisabled = true;

    const el = shallow(<GitImporter {...state} />);

    const site = el
      .find('.c-git-import-step--site')
      .find('.o-collapse-header');

    const main = el
      .find('.c-git-import-step--main')
      .find('.o-collapse-header');

    expect(site.prop('disabled'))
      .to.be.false;

    expect(main.prop('disabled'))
      .to.be.true;
  });

  it(`should render errors`, () => {
    const state = fixtures('git-importer');
    state.errors = [];

    let el = mount(<GitImporter {...state} />);

    expect(el.find('.c-import-error-item'))
      .to.have.length(0);

    state.errors = [{
      type: 'wrong_main_language_exist_in_wagtail',
      details: {
        lang: 'French',
        selected_lang: 'Spanish (Mexico)'
      }
    }, {
      type: 'no_primary_category',
      details: {
        lang: 'Spanish (Mexico)',
        article: 'Palabras sobre el embarazo y el parto'
      }
    }];

    el = mount(<GitImporter {...state} />);

    expect(el.find('.c-import-error-item'))
      .to.have.length(2);
  });

  it(`should call expandStep when user clicks on a completed step`, () => {
    const state = fixtures('git-importer');
    state.steps.main.isDisabled = false;
    state.actions.expandStep = spy();

    const el = shallow(<GitImporter {...state} />);

    el
      .find('.c-git-import-step--main')
      .find('.o-collapse-header')
      .simulate('click');

    expect(state.actions.expandStep.calledWith('main'))
      .to.be.true;

    expect(state.actions.expandStep.calledOnce)
      .to.be.true;
  });
});