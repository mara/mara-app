export default class Window {
    static triggerResize({ delay = 300 } = {}) {
        setTimeout(() => {
            window.dispatchEvent(new Event('resize'));
        }, delay);
    }
}
