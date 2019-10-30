import React from 'react';

import {Column, Row, TextView, CodeView, CardView} from 'Layout/Items.jsx';

import Autosuggest from 'react-autosuggest';

/**
REQUIRED ATTRIBUTES:
this.props.suggestions (an array containing english words suggestions)
this.props.onSubmit (a function to call when a selection is made)

OPTIONAL ATTRIBUTES:
**/
const getSuggestionValue = suggestion => suggestion;

const row_size = 40;
const renderSuggestion = suggestion => (
   <Row styling="primary-highlight" height={row_size + "px"} style = { { "padding" : "0" } } >         
    <Column width="2-3" horizontalAlignment="center" verticalAlignment="center">
      <CardView width="1-1" type="emphasis" fakeLink noShadow>
        <Row height={(row_size-12) + "px"} style={ { "padding" : "5px 2px" } }>
          <Column width="1-1" horizontalAlignment="center" verticalAlignment="center">
              <TextView align="center" text={suggestion} heading={5}/>
          </Column>
        </Row>
      </CardView>
    </Column>
  </Row>
);

export default class AutoCompleteView extends React.Component {
  constructor(props) {
    super(props);

    this.DEBUGGING = false;

    this.state = {
      __value: "",
      __suggestions: []
    };

    // Setting up theme
    this.getSuggestions = this.getSuggestions.bind(this);
    this.getInputProps = this.getInputProps.bind(this);
    // Setting up auto complete functions
    this.onChange = this.onChange.bind(this);
    this.onSuggestionSelected = this.onSuggestionSelected.bind(this);
    this.onSuggestionsFetchRequested = this.onSuggestionsFetchRequested.bind(this);
    this.onSuggestionsClearRequested = this.onSuggestionsClearRequested.bind(this);
    this.getSuggestions = this.getSuggestions.bind(this);
  }

  render() {
    // REQUIRED ATTRIBUTES
    // Suggestions
    let __value = this.state.__value;
    let __inputProps = this.getInputProps(__value);
    
    return (
      <Autosuggest
        suggestions={this.state.__suggestions}
        onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
        onSuggestionsClearRequested={this.onSuggestionsClearRequested}
        onSuggestionSelected={this.onSuggestionSelected}
        getSuggestionValue={getSuggestionValue}
        renderSuggestion={renderSuggestion}
        inputProps={__inputProps}
      />
    );
  }

  getSuggestions(value) {
    var inputValue = "a"; var inputLength = 1; 
    if( typeof value != "undefined") {
      inputValue = value.trim().toLowerCase();
      inputLength = inputValue.length;
    }

    if(this.DEBUGGING) { console.log("DEBUG: Suggestions looked for with: " + inputValue + " of length: " + inputLength); }

    var suggestions = inputLength === 0 ? [] : this.props.suggestions.filter(suggestion =>
      suggestion.toLowerCase().slice(0, inputLength) === inputValue
    );

    if(suggestions.length > 10) { suggestions.splice(10); }

    if(this.DEBUGGING) { console.log("DEBUG: New suggestions found: " + suggestions); }

    return suggestions;
  };

  getInputProps(__value) {
    return {
      placeholder: 'e.g. Darwin Building B05',
      value: __value,
      onChange: this.onChange
    };
  }

  onSuggestionSelected = (event, { suggestion, suggestionValue, suggestionIndex, sectionIndex, method }) => {
    if(this.DEBUGGING) { console.log("DEBUG: Suggestions clicked with a value of: " + suggestionValue); }

    this.props.onSubmit(suggestionValue);
  }

  onChange = (event, { newValue }) => {
    if(this.DEBUGGING) { console.log("DEBUG: Autocomplete form changed input to: " + newValue); }

    this.setState({
      __value: newValue
    });
  };

  // Autosuggest will call this function every time you need to update suggestions.
  // You already implemented this logic above, so just use it.
  onSuggestionsFetchRequested = ({ value }) => {
    if(this.DEBUGGING) { console.log("DEBUG: Fetch suggestions for value of: " + value); }

    this.setState({
      __suggestions: this.getSuggestions(value)
    });
  };

  // Autosuggest will call this function every time you need to clear suggestions.
  onSuggestionsClearRequested = () => {
    if(this.DEBUGGING) { console.log("DEBUG: Cleared suggestions for Autocomplete"); }

    if(!this.DEBUGGING) {
      this.setState({
        __suggestions: []
      });
    }
  };

}