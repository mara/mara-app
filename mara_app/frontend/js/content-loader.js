import Table from '../components/table';
import Alert from '../components/alert';

export default class ContentLoader {
    static loadAndReplace(containerId, url, divHeightKey) {
        const $container = document.getElementById(containerId);

        fetch(url)
            .then(response => response.text())
            .then(content => {
                $container.innerHTML = content;

                Table.reflowMaraTableHeaders();
            })
            .catch(error => {
                Alert.showAlert(
                    `"${error}" while fetching "<a href="${url}">${url}</a>"`,
                    'danger'
                );

                $container.innerHTML = '<span class="fa fa-bug"></span>';
            });
    }
}

window.loadContentAsynchronously = ContentLoader.loadAndReplace;
