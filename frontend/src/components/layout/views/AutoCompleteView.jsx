/* eslint-disable react/prop-types */
// remove this ^ when ready to add prop-types

import React from 'react'
import Autosuggest from 'react-autosuggest'

import { CardView, Column, Row, TextView, Container } from 'Layout/Items.jsx'

/**
REQUIRED ATTRIBUTES:
this.props.suggestions (an array containing english words suggestions)
this.props.onSubmit (a function to call when a selection is made)

OPTIONAL ATTRIBUTES:
**/
const getSuggestionValue = suggestion => suggestion

const row_size = 40
const renderSuggestion = suggestion => (
  <Container styling="primary-highlight" height={row_size + `px`} style={{ "padding": `0` }} >
    <Row width="2-3" horizontalAlignment="center" verticalAlignment="center">
      <CardView width="1-1" type="emphasis" fakeLink noShadow style={{ height: `30px`, paddingTop: `10px` }}>
        <TextView align="center" text={suggestion} heading={5} style={{ margin: `0`, padding: 0 }}/>
      </CardView>
    </Row>
  </Container>
)

export default class AutoCompleteView extends React.Component {
  constructor(props) {
    super(props)

    this.DEBUGGING = false

    this.state = {
      __value: ``,
      __suggestions: [],
    }
  }

  render() {
    // REQUIRED ATTRIBUTES
    // Suggestions
    const { __value, __suggestions } = this.state
    const __inputProps = this.getInputProps(__value)

    return (
      <Autosuggest
        suggestions={__suggestions}
        onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
        onSuggestionsClearRequested={this.onSuggestionsClearRequested}
        onSuggestionSelected={this.onSuggestionSelected}
        getSuggestionValue={getSuggestionValue}
        renderSuggestion={renderSuggestion}
        inputProps={__inputProps}
      />
    )
  }

  getSuggestions = (value) => {
    let inputValue = `a`; let inputLength = 1
    if (typeof value != `undefined`) {
      inputValue = value.trim().toLowerCase()
      inputLength = inputValue.length
    }

    if (this.DEBUGGING) { console.log(`DEBUG: Suggestions looked for with: ` + inputValue + ` of length: ` + inputLength) }

    const { suggestions } = this.props
    const filteredSuggestions = inputLength === 0 ? [] : suggestions.filter(suggestion =>
      suggestion.toLowerCase().slice(0, inputLength) === inputValue
    )

    if (filteredSuggestions.length > 10) { suggestions.splice(10) }

    if (this.DEBUGGING) { console.log(`DEBUG: New suggestions found: ` + filteredSuggestions) }

    return filteredSuggestions
  }

  getInputProps = (__value) => ({
    placeholder: `e.g. Darwin Building B05`,
    value: __value,
    onChange: this.onChange,
  })

  onSuggestionSelected = (event, { suggestionValue /* suggestion, suggestionIndex, sectionIndex, method */ }) => {
    if (this.DEBUGGING) { console.log(`DEBUG: Suggestions clicked with a value of: ` + suggestionValue) }
    const { onSubmit } = this.props
    onSubmit(suggestionValue)
  }

  onChange = (event, { newValue }) => {
    if (this.DEBUGGING) { console.log(`DEBUG: Autocomplete form changed input to: ` + newValue) }

    this.setState({
      __value: newValue,
    })
  };

  // Autosuggest will call this function every time you need to update suggestions.
  // You already implemented this logic above, so just use it.
  onSuggestionsFetchRequested = ({ value }) => {
    if (this.DEBUGGING) { console.log(`DEBUG: Fetch suggestions for value of: ` + value) }

    this.setState({
      __suggestions: this.getSuggestions(value),
    })
  };

  // Autosuggest will call this function every time you need to clear suggestions.
  onSuggestionsClearRequested = () => {
    if (this.DEBUGGING) { console.log(`DEBUG: Cleared suggestions for Autocomplete`) }

    if (!this.DEBUGGING) {
      this.setState({
        __suggestions: [],
      })
    }
  };

}