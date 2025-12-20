'use client';

export default function Navbar() {
  return (
    <nav className="navbar bg-base-100 px-4 py-2">
      <div className="navbar-start">
        <div className="dropdown">
          <div tabIndex={0} role="button" className="btn btn-ghost">
            Categories
          </div>
          <ul tabIndex={0} className="dropdown-content menu bg-base-100 shadow">
            <li>
              <a>Item 1</a>
            </li>
            <li>
              <a>Item 2</a>
            </li>
          </ul>
        </div>
        <div className="dropdown">
          <div tabIndex={0} role="button" className="btn btn-ghost">
            New Product
          </div>
          <ul tabIndex={0} className="dropdown-content menu bg-base-100 shadow">
            <li>
              <a>Item 1</a>
            </li>
            <li>
              <a>Item 2</a>
            </li>
          </ul>
        </div>
      </div>
      <div className="navbar-center">
        <div className="form-control">
          <div className="input-group">
            <input
              type="text"
              placeholder="Search"
              className="input input-bordered w-full max-w-xs"
            />
            <button className="btn btn-square">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                className="w-5 h-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div className="navbar-end gap-2">
        <button className="btn btn-ghost">Men</button>
        <button className="btn btn-ghost">Women</button>
        <button className="btn btn-ghost">Children</button>
        <button className="btn btn-ghost">Brand</button>
      </div>
    </nav>
  );
}

