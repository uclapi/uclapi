import RelativeLayout from '../containers/RelativeLayout.jsx';

class RelativeLayoutNode {
  
  constructor() {
    this.children = [];
  }

  add(children) {
    children.forEach(function(child) {
      this.children.push(child);
    });
  }

  getView() {
    return <RelativeLayout>
              {this.children.map((child) => child.getView())}
           </RelativeLayout>
  }
}