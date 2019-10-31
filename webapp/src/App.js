import React from 'react';

function App() {
  return (
    <div>
      <nav className="navbar navbar-dark bg-dark">
        <span className="navbar-brand">NUesc</span>

        <span class="text-white">Prototype</span>
      </nav>

      <div className="container-fluid mt-3">
        <div className="row">
          <div className="col-4">
            <h3 className="text-center">Sound List</h3>
            <hr/>

            <form>
              <div className="form-group">
                <select className="custom-select">
                  <option value="">1</option>
                  <option value="">2</option>
                  <option value="">3</option>
                </select>
              </div>

              <div className="form-group">
                <input type="submit" className="btn btn-success w-100" value="Set in Pi" />
              </div>
            </form>
          </div>
          <div className="col-8">
            <h3 className="text-center">Raspberry Pi</h3>
            <hr/>

            <div className="container">
              <div className="alert alert-success" role="alert">
                <b>Status: </b> <span id="pi-status">Listening to Dog Bark</span>
              </div>

              <div className="text-center mt-5 text-danger">
                <h1 id="detected">Dog Bark Detected !</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  );
}

export default App;
