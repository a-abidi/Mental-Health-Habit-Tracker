import React from "react";
import Popup from "../Popup";

export default class MenuContainer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showPopup: false,
      activeItem: "",
      activeItemPosition: 0,
      activeItemColor: "",
      //Items to be displayed
      menuItems: [
        { text: "Mental Health" },
        { text: "Adjustments" },
        { text: "Self-confidence" }
      ]
    };
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.togglePopup = this.togglePopup.bind(this);
  }

  togglePopup() {
    this.setState({
      showPopup: !this.state.showPopup
    });
  }

  handleMouseOver(activeItem) {
    return e => {
      e.preventDefault();
      console.log(this.state.activeItem);
      this.setState({
        activeItem,
        activeItemPosition: document.getElementById(activeItem).offsetTop,
        activeItemColor: window
          .getComputedStyle(document.getElementById(activeItem))
          .getPropertyValue("background-color")
      });
    };
  }

  render() {
    const menuItems = this.state.menuItems.map(item => (
      <MenuItem
        item={item}
        handleMouseOver={this.handleMouseOver}
        togglePopup={this.togglePopup}
      />
    ));
    return (
      <div className="menu-container">
        <span
          className="menu-item--active"
          style={{
            top: this.state.activeItemPosition,
            backgroundColor: this.state.activeItemColor
          }}
        />
        {menuItems}
        {this.state.showPopup ? (
          <Popup
            text="Close Me"
            closePopup={this.togglePopup}
            questionaire={this.state.activeItem}
          />
        ) : null}
      </div>
    );
  }
}

//Menu item component
function MenuItem(props) {
  return (
    <div
      className="menu-item"
      id={props.item.text}
      onMouseOver={props.handleMouseOver(props.item.text)}
      onClick={props.togglePopup}
    >
      {props.item.text.toUpperCase()}
    </div>
  );
}
