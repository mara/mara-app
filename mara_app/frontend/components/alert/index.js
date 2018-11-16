import './index.scss';

export default class Alert {
    // adds an alert to the bottom of the page
    static showAlert(message, category) {
        const $alerts = document.getElementById('alerts');

        const $alert = document.createElement('div');
        $alert.classList.add(
            'alert',
            'alert--hidden',
            `alert-${category}`,
            `alert-dismissible`
        );
        $alert.innerHTML = `
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
            ${message}
        `;

        $alerts.appendChild($alert);

        setTimeout(() => {
            $alert.classList.remove('alert--hidden');
        }, 1000);
    }
}
