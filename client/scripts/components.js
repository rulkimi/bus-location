class Card extends HTMLElement {
  constructor() {
      super();
      this.innerHTML = `
          <div class="card">
              this is a card.
          </div>
      `;
  }
}

class Header extends HTMLElement {
  constructor() {
      super();
      this.innerHTML = `
          <div class="card">
              this is a header.
          </div>
      `;
  }
}

customElements.define('my-card', Card);
customElements.define('my-header', Header);